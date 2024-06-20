from pydantic import BaseModel
from ..models.db_field_info import DbField
from .verify_subclasses import is_subclass
from .aggregate_stages import (
    unwind,
    group_set_replace_root,
    unset,
    lookup,
    set_,
)
import copy


def _paths_to_ref_ids(
    cls: BaseModel,
    paths: list,
    db_field_path: list,
    populate_db_fields: list[DbField] | None,
):
    for field in cls.model_fields:
        try:
            db_field: DbField = getattr(cls, field)
        except AttributeError:
            if is_subclass(class_to_verify=cls, subclass=BaseModel):
                raise TypeError(
                    f"The {cls.__name__} class inherits from Pydantic's BaseModel class. Try switching to PyODMongo's MainBaseModel class"
                )
        db_field_path.append(db_field)
        if db_field.by_reference:
            try:
                if db_field in populate_db_fields:
                    paths.append(copy.deepcopy(db_field_path))
            except TypeError:
                paths.append(copy.deepcopy(db_field_path))
        elif db_field.has_model_fields:
            _paths_to_ref_ids(
                cls=db_field.field_type,
                paths=paths,
                db_field_path=db_field_path,
                populate_db_fields=populate_db_fields,
            )
        db_field_path.pop(-1)
    return paths


def resolve_reference_pipeline(
    cls: BaseModel, pipeline: list, populate_db_fields: list[DbField] | None
):
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
    paths = _paths_to_ref_ids(
        cls=cls, paths=[], db_field_path=[], populate_db_fields=populate_db_fields
    )
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
            pipeline=resolve_reference_pipeline(
                cls=db_field.field_type,
                pipeline=[],
                populate_db_fields=populate_db_fields,
            ),
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
