from pydantic import BaseModel
from bson import ObjectId


class MainModel(BaseModel):
    def __init_subclass__(cls, **kwargs):
        for key, value in cls.__fields__.items():
            setattr(cls, value.name, (value.name, value.type_))

    class Config:
        json_encoders = {ObjectId: str}
