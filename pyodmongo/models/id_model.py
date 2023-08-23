from typing import Annotated, Any
from bson import ObjectId
from bson.errors import InvalidId
from ..pydantic_version import is_pydantic_v1
if not is_pydantic_v1:
    from pyodmongo import GetCoreSchemaHandler
    from pydantic_core import core_schema, CoreSchema
    from pydantic_core.core_schema import ValidationInfo, str_schema


class Id(str):
    
    if not is_pydantic_v1:
        @classmethod
        def validate(cls, v, _: ValidationInfo):
            if not ObjectId.is_valid(v):
                raise ValueError('invalid Id')
            return str(v)

        @classmethod
        def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
        ) -> CoreSchema:  # type: ignore
            return core_schema.json_or_python_schema(
                python_schema=core_schema.general_plain_validator_function(
                    cls.validate
                ),
                json_schema=str_schema(),
                serialization=core_schema.plain_serializer_function_ser_schema(
                    lambda instance: str(instance)
                ),
            )
    
    else:
        @classmethod
        def __get_validators__(cls):
            yield cls.validate
        
        @classmethod
        def validate(cls, v):
            if not ObjectId.is_valid(v):
                raise ValueError('invalid Id')
            return str(v)