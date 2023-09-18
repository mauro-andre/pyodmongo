from .meta import PyODMongoMeta
from pydantic import BaseModel, ConfigDict
from .id_model import Id
from datetime import datetime
from typing import ClassVar
from ..services.model_init import resolve_indexes, resolve_ref_pipeline, resolve_class_fields_db_info


class DbModel(BaseModel, metaclass=PyODMongoMeta):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None
    model_config = ConfigDict(populate_by_name=True)
    _pipeline: ClassVar = []

    def __init__(self, **attrs):
        if attrs.get('_id') is not None:
            attrs['id'] = attrs.pop('_id')
        super().__init__(**attrs)

    @classmethod
    def __pydantic_init_subclass__(cls):
        resolve_class_fields_db_info(cls=cls)
        ref_pipeline = resolve_ref_pipeline(cls=cls, pipeline=[], path=[])
        setattr(cls, '_reference_pipeline', ref_pipeline)
        indexes = resolve_indexes(cls=cls)
        setattr(cls, '_init_indexes', indexes)
