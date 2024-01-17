from pydantic import ConfigDict
from pydantic_dbmodel_core import DbModelCore
from .id_model import Id
from datetime import datetime
from typing import ClassVar
from ..services.model_init import (
    resolve_indexes,
    resolve_ref_pipeline,
    resolve_class_fields_db_info,
    resolve_project_pipeline,
)


class DbModel(DbModelCore):
    id: Id | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(populate_by_name=True)
    _pipeline: ClassVar = []

    def __init__(self, **attrs):
        for key, value in attrs.items():
            if value == {}:
                attrs[key] = None
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
        project_pipeline = resolve_project_pipeline(cls=cls)
        setattr(cls, "_project_pipeline", project_pipeline)
