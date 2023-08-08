from typing_extensions import Annotated
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BeforeValidator

def obj_id_to_string(value):
    try:
        return str(ObjectId(value))
    except InvalidId as e:
        raise ValueError('invalid Id')
    
Id = Annotated[str, BeforeValidator(obj_id_to_string)]