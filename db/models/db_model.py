from .main_model import MainModel
from ..services.db_model_init import resolve_indexes, resolve_lookup_and_set
from .id_model import Id
from datetime import datetime
from ..services.db_model_init import field_infos
from ..models.field_info import FieldInfo


class DbModel(MainModel):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None
    _pipeline: list = []

    def __init__(self, **attrs):
        if attrs.get('_id') is not None:
            attrs['id'] = attrs.pop('_id')
        super().__init__(**attrs)

    def __init_subclass__(cls):
        ref_pipeline = resolve_lookup_and_set(cls=cls, pipeline=[], path='')
        indexes = resolve_indexes(cls=cls)
        for key in cls.__fields__.keys():
            field_info: FieldInfo = field_infos(cls=cls, field_name=key)
            setattr(cls, key, field_info)
        setattr(cls, '_indexes', indexes)
        setattr(cls, '_reference_pipeline', ref_pipeline)

    @classmethod
    def populate(cls):
        print(cls)

    class Config:
        anystr_strip_whitespace = True
