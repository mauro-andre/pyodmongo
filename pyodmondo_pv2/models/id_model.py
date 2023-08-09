from typing import Annotated
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BeforeValidator

def _id(value):
    try:
        return str(ObjectId(value))
    except InvalidId as e:
        raise ValueError('invalid Id')
    
Id = Annotated[str, BeforeValidator(_id), '_id']