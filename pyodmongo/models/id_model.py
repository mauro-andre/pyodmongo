from typing import Any
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema, CoreSchema
from pydantic_core.core_schema import ValidationInfo, str_schema


class Id(str):

    @classmethod
    def validate(cls, v, _: ValidationInfo):
        if v is None:
            return v
        if not ObjectId.is_valid(v):
            raise ValueError('invalid Id')
        return str(v)

    @classmethod
    def serialization(cls, v):
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
                lambda v: str(v) if ObjectId.is_valid(v) else v
            ),
        )

    # @classmethod
    # def __get_pydantic_json_schema__(
    #     cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler  # type: ignore
    # ) -> JsonSchemaValue:
    #     json_schema = handler(schema)
    #     # json_schema.update(
    #     #     type="string",
    #     #     example="5eb7cf5a86d9755df3a6c593",
    #     # )
    #     return json_schema
