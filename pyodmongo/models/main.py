from .meta import PyODMongoMeta
from .id_model import Id
from pydantic import BaseModel
from datetime import datetime


class DbModel(BaseModel, metaclass=PyODMongoMeta):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None
