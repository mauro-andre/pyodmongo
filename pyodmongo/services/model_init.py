from pydantic import BaseModel
from pymongo import IndexModel, ASCENDING, TEXT
from typing import Any, Union, get_origin, get_args
from types import UnionType
from ..models.id_model import Id
from ..models.db_field_info import DbField
from .aggregate_stages import lookup_and_set


def resolve_indexes(cls: BaseModel):
    indexes = []
    text_keys = []
    for key in cls.model_fields.keys():
        is_index = cls.model_fields[key]._attributes_set.get("index") or False
        is_unique = cls.model_fields[key]._attributes_set.get("unique") or False
        is_text_index = cls.model_fields[key]._attributes_set.get("text_index") or False
        default_language = (
            cls.model_fields[key]._attributes_set.get("default_language") or False
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
    by_reference = (Id in args) and (field != "id")
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


def resolve_project_pipeline(cls: BaseModel, path: list):
    project = {}
    for field, field_info in cls.model_fields.items():
        db_field_info = field_annotation_infos(field=field, field_info=field_info)
        path.append(db_field_info.field_alias)
        path_str = ".".join(path)
        project[path_str] = True
        if db_field_info.has_model_fields:
            if not db_field_info.by_reference:
                project.pop(path_str)
                project.update(
                    resolve_project_pipeline(cls=db_field_info.field_type, path=path)
                )
        path.pop(-1)
    return project


def resolve_ref_pipeline(cls: BaseModel, pipeline: list, path: list):
    for field, field_info in cls.model_fields.items():
        db_field_info = field_annotation_infos(field=field, field_info=field_info)
        path.append(db_field_info.field_alias)
        path_str = ".".join(path)
        if db_field_info.has_model_fields:
            if db_field_info.by_reference:
                collection = db_field_info.field_type._collection
                pipeline += lookup_and_set(
                    from_=collection,
                    local_field=path_str,
                    foreign_field="_id",
                    as_=path_str,
                    pipeline=resolve_ref_pipeline(
                        cls=db_field_info.field_type, pipeline=[], path=[]
                    ),
                    is_reference_list=db_field_info.is_list,
                )
            else:
                resolve_ref_pipeline(
                    cls=db_field_info.field_type,
                    pipeline=pipeline,
                    path=path,
                )
        path.pop(-1)
    # project = resolve_project_pipeline(cls=cls, path=[])
    # try:
    #     project_index = [list(dct.keys())[0] for dct in pipeline].index("$project")
    #     pipeline[project_index] = {"$project": project}
    # except ValueError:
    #     pipeline += [{"$project": project}]
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
    for field, field_info in cls.model_fields.items():
        db_field_info = field_annotation_infos(field=field, field_info=field_info)
        path = db_field_info.field_alias
        db_field_info.path_str = path
        field_to_set = _recursice_db_fields_info(
            db_field_info=db_field_info, path=[path]
        )
        setattr(cls, field, field_to_set)
