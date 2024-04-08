from pydantic import ConfigDict
from pydantic_dbmodel_core import DbModelCore
from .id_model import Id
from datetime import datetime
from typing import ClassVar
from ..services.model_init import (
    resolve_indexes,
    resolve_ref_pipeline,
    resolve_class_fields_db_info,
)


class DbModel(DbModelCore):
    id: Id | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(populate_by_name=True)
    _pipeline: ClassVar = []

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

    @classmethod
    def __pydantic_init_subclass__(cls):
        resolve_class_fields_db_info(cls=cls)
        ref_pipeline = resolve_ref_pipeline(cls=cls, pipeline=[], path=[])
        setattr(cls, "_reference_pipeline", ref_pipeline)
        indexes = resolve_indexes(cls=cls)
        setattr(cls, "_init_indexes", indexes)
