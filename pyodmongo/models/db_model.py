# from pydantic.main import BaseModel, ConfigDict
# from ..services.db_model_init import resolve_indexes, resolve_lookup_and_set, set_new_field_info
# from .id_model import Id
# from datetime import datetime
# from dataclasses import dataclass
# # @dataclass


# class DbModel(BaseModel):
#     id: Id = None
#     created_at: datetime = None
#     updated_at: datetime = None
#     model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

#     def __init__(self, **attrs):
#         if attrs.get('_id') is not None:
#             attrs['id'] = attrs.pop('_id')
#         super().__init__(**attrs)

#     @classmethod
#     def __pydantic_init_subclass__(cls):
#         ref_pipeline = resolve_lookup_and_set(cls=cls, pipeline=[], path=[])
#         indexes = resolve_indexes(cls=cls)
#         # set_new_field_info(cls=cls)
#         setattr(cls, '_pipeline', [])
#         setattr(cls, '_indexes', indexes)
#         setattr(cls, '_reference_pipeline', ref_pipeline)

from ..pydantic_mod.main import BaseModel
from .id_model import Id
from datetime import datetime
from ..services.model_init import resolve_indexes


class DbModel(BaseModel):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None

    def __init__(self, **attrs):
        if attrs.get('_id') is not None:
            attrs['id'] = attrs.pop('_id')
        super().__init__(**attrs)

    @classmethod
    def __pydantic_init_subclass__(cls):
        indexes = resolve_indexes(cls=cls)
        setattr(cls, '_indexes', indexes)
        for field in cls.model_fields:
            setattr(cls, field, 'TEMP VALUE')
        pass
