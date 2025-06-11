from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.fields import FieldInfo
from typing_extensions import dataclass_transform
from typing import Any, Union, List, get_args, get_origin
from types import UnionType
from ..models.id_model import Id
from ..models.db_field import DbField


def _resolve_db_field(
    field_name: str, field_info: FieldInfo, db_field: DbField, path: list
) -> DbField:
    db_field.field_name = field_name
    db_field.field_alias = (
        field_info.alias or field_name if field_name != "id" else "_id"
    )
    annotation = field_info.annotation

    def is_union(value) -> bool:
        return get_origin(value) is UnionType or get_origin(value) is Union

    db_field.is_union = is_union(value=annotation)
    db_field.is_list = get_origin(annotation) is list or get_origin(annotation) is List
    if db_field.is_union:
        args = get_args(annotation)
        db_field.types = list(args)
    elif db_field.is_list:
        args = get_args(annotation)[0]
        db_field.is_union = is_union(value=args)
        if db_field.is_union:
            args = get_args(args)
            db_field.types = list(args)
        else:
            db_field.types = [args]
    else:
        db_field.types = [annotation]
    db_field.by_reference = Id in db_field.types
    path.append(db_field.field_alias)
    db_field.path_str = ".".join(path)

    for cls in db_field.types:
        if not hasattr(cls, "model_fields"):
            continue
        for inner_field_name, inner_field_info in cls.model_fields.items():
            setattr(db_field, inner_field_name, DbField())
            _resolve_db_field(
                field_name=inner_field_name,
                field_info=inner_field_info,
                db_field=getattr(db_field, inner_field_name),
                path=path,
            )
            path.pop()
    return db_field


def _resolve_cls_db_fields(cls):
    for field_name, field_info in cls.model_fields.items():
        db_field = DbField()
        db_field = _resolve_db_field(
            field_name=field_name, field_info=field_info, db_field=db_field, path=[]
        )
        setattr(cls, field_name + "__db_field", db_field)


# def _resolve_field_db_dict(
#     field_name: str, field_info: FieldInfo, db_dict: dict
# ) -> dict:
#     field_alias = field_info.alias or field_name if field_name != "id" else "_id"
#     annotation = field_info.annotation

#     def _is_union(value) -> bool:
#         return get_origin(value) is UnionType or get_origin(value) is Union

#     is_union = _is_union(value=annotation)
#     is_list = get_origin(annotation) is list or get_origin(annotation) is List

#     db_dict[field_name] = (None, "Alguma coisa")
#     print(annotation)
#     return db_dict


# def _resolve_cls_db_dict(cls):
#     db_dict = {}
#     for field_name, field_info in cls.model_fields.items():
#         db_dict = _resolve_field_db_dict(
#             field_name=field_name, field_info=field_info, db_dict=db_dict
#         )
#     setattr(cls, "__db_dict__", db_dict)
#     print(cls.__dict__.get("__db_dict__"))
#     print()


@dataclass_transform(kw_only_default=True)
class MainMeta(ModelMetaclass):

    def __new__(
        cls, name: str, bases: tuple[Any], namespace: dict, **kwargs: Any
    ) -> type:
        setattr(cls, "__main_meta_complete__", False)
        for base in bases:
            setattr(base, "__main_meta_complete__", False)

        cls: BaseModel = ModelMetaclass.__new__(cls, name, bases, namespace, **kwargs)

        setattr(cls, "__main_meta_complete__", True)
        for base in bases:
            setattr(base, "__main_meta_complete__", True)

        _resolve_cls_db_fields(cls=cls)
        # _resolve_cls_db_dict(cls=cls)
        return cls

    def __getattr__(cls, name: str):
        # if cls.__dict__.get("__main_meta_complete__") and cls.__dict__.get("__db_dict__"):
        #     print(cls.__dict__.get("__db_dict__"))
        #     print()

        if cls.__dict__.get("__main_meta_complete__") and cls.__dict__.get(
            name + "__db_field"
        ):
            return cls.__dict__.get(name + "__db_field")
        # # if (
        #     cls.__dict__.get("__main_meta_complete__")
        #     and "__db_fields__" in cls.__dict__
        #     and name in cls.__dict__["__db_fields__"]
        # ):
        #     db_field: DbField = cls.__dict__["__db_fields__"][name]
        #     return db_field
        return ModelMetaclass.__getattr__(cls, name)
