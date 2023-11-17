from typing import Any
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
import pydantic_core
from pydantic_core import core_schema, CoreSchema
from pydantic_core.core_schema import ValidationInfo, str_schema
from packaging import version


class Id(str):
    @classmethod
    def validate(cls, v, _: ValidationInfo):
        if v is None:
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("invalid Id")
        return str(v)

    @classmethod
    def serialization(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("invalid Id")
        return str(v)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:  # type: ignore
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v) if ObjectId.is_valid(v) else v
            ),
        )
