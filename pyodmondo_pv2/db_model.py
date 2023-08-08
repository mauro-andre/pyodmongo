from pydantic import BaseModel
# from ..services.db_model_init import resolve_indexes, resolve_lookup_and_set, set_new_field_info
from .id_model import Id
from datetime import datetime
# from ..models.field_info import FieldInfo


class DbModel(BaseModel):
    id: Id = 123
    created_at: datetime = None
    updated_at: datetime = None
    _pipeline: list = []

    def __init__(self, **attrs):
        if attrs.get('_id') is not None:
            attrs['id'] = attrs.pop('_id')
        super().__init__(**attrs)

    # def __init_subclass__(cls):
    #     ref_pipeline = resolve_lookup_and_set(cls=cls, pipeline=[], path=[])
    #     indexes = resolve_indexes(cls=cls)
    #     set_new_field_info(cls=cls)
    #     setattr(cls, '_indexes', indexes)
    #     setattr(cls, '_reference_pipeline', ref_pipeline)

    # class Config:
    #     anystr_strip_whitespace = True
    #     validate_assignment = True
