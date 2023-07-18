from pydantic import BaseModel
from bson import ObjectId


class MainModel(BaseModel):

    class Config:
        json_encoders = {ObjectId: str}
