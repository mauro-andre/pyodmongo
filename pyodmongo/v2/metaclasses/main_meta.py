from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.fields import FieldInfo
from typing_extensions import dataclass_transform
from typing import Any, Union, List, get_args, get_origin
from types import UnionType
from ..models.id_model import Id


class DbField:
    def __init__(self):
        self.field_name = None
        self.field_alias = None
        self.path_str = None
        # self.annotation = None
        self.by_reference = None
        self.is_list = None
        self.is_union = None
        self.types = []
        # self.has_model_fields = None

    def __repr__(self):
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"DbField({attrs_str})"


def _resolve_db_field(
    field_name: str, field_info: FieldInfo, db_field: DbField
) -> DbField:
    db_field.field_name = field_name
    db_field.field_alias = field_info.alias or field_name
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

    for cls in db_field.types:
        if not hasattr(cls, "model_fields"):
            continue
        cls: BaseModel
        for inner_field_name, inner_field_info in cls.model_fields.items():
            setattr(db_field, inner_field_name, DbField())
            _resolve_db_field(
                field_name=inner_field_name,
                field_info=inner_field_info,
                db_field=getattr(db_field, inner_field_name),
            )
    return db_field


def _resolve_cls_db_fields(cls: BaseModel):
    for field_name, field_info in cls.model_fields.items():
        db_field = DbField()
        db_field = _resolve_db_field(
            field_name=field_name, field_info=field_info, db_field=db_field
        )
        setattr(cls, field_name, db_field)


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
        return cls

    def __getattr__(cls, name: str):
        if cls.__dict__.get("__main_meta_complete__") and cls.__dict__.get(
            name + "__main_meta"
        ):
            return cls.__dict__.get(name + "__main_meta")
        return ModelMetaclass.__getattr__(cls, name)
