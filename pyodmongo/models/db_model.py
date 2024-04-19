from pydantic import ConfigDict
from .id_model import Id
from datetime import datetime
from typing import ClassVar
from ..services.model_init import (
    resolve_indexes,
    resolve_class_fields_db_info,
    resolve_reference_pipeline,
)
from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from abc import ABCMeta
from typing_extensions import dataclass_transform
from typing import ClassVar


class PyOdmongoMeta(ABCMeta):
    def __getattr__(cls, name: str):
        if cls.__dict__.get("pyodmongo_complete"):
            is_attr = name in cls.__dict__["model_fields"].keys()
            if is_attr:
                return cls.__dict__.get(name + "__pyodmongo")
        ModelMetaclass.__getattr__(cls, name)


@dataclass_transform()
class DbMeta(PyOdmongoMeta, ModelMetaclass): ...


class DbModel(BaseModel, metaclass=DbMeta):
    id: Id | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(populate_by_name=True)
    _pipeline: ClassVar = []

    @classmethod
    def __init_subclass__(cls):
        setattr(cls, "pyodmongo_complete", False)
        for base in cls.__bases__:
            setattr(base, "pyodmongo_complete", False)

    @classmethod
    def __pydantic_init_subclass__(cls):
        setattr(cls, "pyodmongo_complete", True)
        for base in cls.__bases__:
            setattr(base, "pyodmongo_complete", True)
        resolve_class_fields_db_info(cls=cls)
        pipeline = resolve_reference_pipeline(cls=cls, pipeline=[])
        setattr(cls, "_reference_pipeline", pipeline)
        indexes = resolve_indexes(cls=cls)
        setattr(cls, "_init_indexes", indexes)

    def __remove_empty_dict(self, dct: dict):
        for key, value in dct.items():
            if value == {}:
                dct[key] = None
            elif type(value) == dict:
                self.__remove_empty_dict(dct=value)
                is_full_empty = all(
                    v == None or v == {} or v == [] for v in value.values()
                )
                if is_full_empty:
                    dct[key] = None
        if dct == {}:
            return None
        else:
            return dct

    def __init__(self, **attrs):
        for key, value in attrs.items():
            if type(value) == dict:
                attrs[key] = self.__remove_empty_dict(dct=value)
        if attrs.get("_id") is not None:
            attrs["id"] = attrs.pop("_id")
        super().__init__(**attrs)
