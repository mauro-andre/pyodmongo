from pydantic import BaseModel
from pymongo import IndexModel, ASCENDING, TEXT
from typing import Any, Union, get_origin, get_args
from types import UnionType
from ..models.id_model import Id
from ..models.db_field_info import DbField
from .aggregate_stages import (
    unwind,
    group_set_replace_root,
    unset,
    lookup,
    set_,
)
import copy


def resolve_indexes(cls: BaseModel):
    """
    Resolves and constructs MongoDB index models for the fields of a given class based on field attributes.

    Args:
        cls (BaseModel): The model class whose indexes are to be resolved.

    Returns:
        list[IndexModel]: A list of MongoDB index models constructed for the class fields.

    Description:
        This method iterates over the model fields and checks for index-related attributes (index, unique,
        text_index). It creates appropriate MongoDB index structures (IndexModel) for these fields,
        including handling of text indexes and unique constraints.
    """
    indexes = []
    text_keys = []
    for key in cls.model_fields.keys():
        if not cls.model_fields[key].json_schema_extra:
            continue
        is_index = cls.model_fields[key].json_schema_extra.get("index") or False
        is_unique = cls.model_fields[key].json_schema_extra.get("unique") or False
        is_text_index = (
            cls.model_fields[key].json_schema_extra.get("text_index") or False
        )
        default_language = (
            cls.model_fields[key].json_schema_extra.get("default_language") or False
        )
        db_field_info: DbField = getattr(cls, key)
        alias = db_field_info.field_alias
        if is_index:
            indexes.append(
                IndexModel([(alias, ASCENDING)], name=alias, unique=is_unique)
            )
        if is_text_index:
            text_keys.append((alias, TEXT))
    if len(text_keys) > 0:
        if default_language:
            indexes.append(
                IndexModel(text_keys, name="texts", default_language=default_language)
            )
        else:
            indexes.append(IndexModel(text_keys, name="texts"))

    return indexes


def _is_union(field_type: Any):
    return get_origin(field_type) is UnionType or get_origin(field_type) is Union


def _has_a_list_in_union(field_type: Any):
    for ft in get_args(field_type):
        if get_origin(ft) is list:
            return ft


def _union_collector_info(field, args):
    args = get_args(args)
    has_any_model_field = False
    for arg in args:
        if hasattr(arg, "model_fields"):
            has_any_model_field = True
    by_reference = (Id in args) and (field != "id") and has_any_model_field
    if by_reference:
        field_type_index = 0
        for arg in args:
            if hasattr(arg, "model_fields"):
                break
            field_type_index += 1
        field_type = args[field_type_index]
    else:
        field_type = args[0]
    return field_type, by_reference


def field_annotation_infos(field, field_info) -> DbField:
    """
    Extracts and constructs database field metadata from model field annotations.

    Args:
        field (str): The name of the field in the model.
        field_info (Field): Pydantic model field information containing metadata.

    Returns:
        DbField: A DbField instance encapsulating the database-related metadata of the model field.

    Description:
        This method processes a model field's annotation to determine its database-related properties,
        such as whether it's a list, reference, or contains sub-model fields. It constructs and returns
        a DbField object that represents this metadata.
    """
    field_annotation = field_info.annotation
    by_reference = False
    field_type = field_annotation
    if _is_union(field_type=field_annotation):
        has_a_list_in_union = _has_a_list_in_union(field_type=field_annotation)
        if has_a_list_in_union is not None:
            field_annotation = has_a_list_in_union
    is_list = get_origin(field_annotation) is list
    if is_list:
        args = get_args(field_annotation)[0]
        is_union = _is_union(args)
        if is_union:
            field_type, by_reference = _union_collector_info(field=field, args=args)
        else:
            field_type = args
    elif _is_union(field_annotation):
        field_type, by_reference = _union_collector_info(
            field=field, args=field_annotation
        )
    has_model_fields = hasattr(field_type, "model_fields")
    field_name = field
    field_alias = field_info.alias or field
    if field_name == "id":
        field_alias = "_id"
    return DbField(
        field_name=field_name,
        field_alias=field_alias,
        field_type=field_type,
        by_reference=by_reference,
        is_list=is_list,
        has_model_fields=has_model_fields,
    )


def _paths_to_ref_ids(cls: BaseModel, paths: list, db_field_path: list):
    for field, field_info in cls.model_fields.items():
        db_field = field_annotation_infos(field=field, field_info=field_info)
        db_field_path.append(db_field)
        if db_field.by_reference:
            paths.append(copy.deepcopy(db_field_path))
        elif db_field.has_model_fields:
            _paths_to_ref_ids(
                cls=db_field.field_type, paths=paths, db_field_path=db_field_path
            )
        db_field_path.pop(-1)
    return paths


def resolve_reference_pipeline(cls: BaseModel, pipeline: list):
    """
    Constructs a MongoDB aggregation pipeline that handles document references within a given class model.

    Args:
        cls (BaseModel): The model class for which to build the reference resolution pipeline.
        pipeline (list): Initial pipeline stages to which reference resolution stages will be added.

    Returns:
        list: The modified MongoDB aggregation pipeline including reference resolution stages.

    Description:
        This function builds a pipeline that unwinds arrays, performs lookups for references, and resets
        document structures to correctly embed referenced documents. It supports nested models and handles
        complex reference structures.
    """
    paths = _paths_to_ref_ids(cls=cls, paths=[], db_field_path=[])
    for db_field_path in paths:
        path_str = ""
        unwind_index_list = []
        paths_str_to_group = []
        db_field: DbField = None
        for index, db_field in enumerate(db_field_path):
            db_field: DbField
            path_str += (
                "." + db_field.field_alias if path_str != "" else db_field.field_alias
            )

            if db_field.is_list and not db_field.by_reference:
                unwind_index_list.append(f"__unwind_{index}")
                paths_str_to_group.append(path_str)
                pipeline += unwind(
                    path=path_str,
                    array_index=unwind_index_list[-1],
                    preserve_empty=True,
                )

        pipeline += lookup(
            from_=db_field.field_type._collection,
            local_field=path_str,
            foreign_field="_id",
            as_=path_str,
            pipeline=resolve_reference_pipeline(cls=db_field.field_type, pipeline=[]),
        )
        if not db_field.is_list:
            pipeline += set_(as_=path_str)

        for index, path_str in enumerate(reversed(paths_str_to_group)):
            reverse_index = len(paths_str_to_group) - index - 1
            unwind_index = (
                "_id" if reverse_index - 1 < 0 else unwind_index_list[reverse_index - 1]
            )
            pipeline += group_set_replace_root(
                id_=unwind_index, field=path_str.split(".")[-1], path_str=path_str
            )
            pipeline += unset(fields=[unwind_index_list[reverse_index - 1]])

    return pipeline


def _recursice_db_fields_info(db_field_info: DbField, path: list) -> DbField:
    if db_field_info.has_model_fields:
        for field, field_info in db_field_info.field_type.model_fields.items():
            rec_db_field_info = field_annotation_infos(
                field=field, field_info=field_info
            )
            path.append(rec_db_field_info.field_alias)
            path_str = ".".join(path)
            rec_db_field_info.path_str = path_str
            rec_db_field_info = _recursice_db_fields_info(
                db_field_info=rec_db_field_info, path=path
            )
            setattr(db_field_info, field, rec_db_field_info)
    path.pop(-1)
    return db_field_info


def resolve_class_fields_db_info(cls: BaseModel):
    """
    Resolves and sets database field information for all fields of the specified class.

    Args:
        cls (BaseModel): The class whose fields are to be resolved.

    Description:
        This method iterates over each field of the given class, resolves its database field information,
        and sets additional properties directly on the class to facilitate database operations. This includes
        constructing nested DbField structures for complex models.
    """
    for field, field_info in cls.model_fields.items():
        db_field_info = field_annotation_infos(field=field, field_info=field_info)
        path = db_field_info.field_alias
        db_field_info.path_str = path
        field_to_set = _recursice_db_fields_info(
            db_field_info=db_field_info, path=[path]
        )
        setattr(cls, field + "__pyodmongo", field_to_set)


# TODO finish resolve_single_db_field
# def resolve_single_db_field(value: Any) -> DbField:
#     by_reference = False
#     return value


# def resolve_db_fields(bases: tuple[Any], db_fields: dict):
#     for base in bases:
#         if base is object:
#             continue
#         base_annotations = base.__dict__.get("__annotations__")
#         for base_field, value in base_annotations.items():
#             if base_field not in db_fields.keys() and not base_field.startswith("_"):
#                 db_fields[base_field] = resolve_single_db_field(value=value)
#         resolve_db_fields(bases=base.__bases__, db_fields=db_fields)
#     return db_fields
