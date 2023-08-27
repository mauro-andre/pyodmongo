from ..pydantic_mod.main import BaseModel, ConfigDict
from .id_model import Id
from datetime import datetime
from ..services.model_init import resolve_indexes, resolve_ref_pipeline, resolve_class_fields_db_info


class DbModel(BaseModel):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None
    model_config = ConfigDict(populate_by_name=True)
    # TODO set a _collection default for autocomplete and validate to raise an error if not filled

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
        setattr(cls, '_indexes', indexes)
        setattr(cls, '_pipeline', [])
        if not hasattr(cls, '_collection'):
            raise AttributeError(f"Model {cls.__name__} has no '_collection: typing.ClassVar'")
