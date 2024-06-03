from typing import Any
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema, CoreSchema
from pydantic_core.core_schema import ValidationInfo, str_schema


class Id(str):
    """
    Extends the base string type to implement custom validation and serialization logic
    specifically for IDs that are expected to be in MongoDB's ObjectId format. This class
    ensures that IDs are valid ObjectIds and can be used consistently throughout the model
    where ID validation and serialization are necessary.

    Methods:
        validate(cls, v, _): Validates that the given value `v` is a valid ObjectId. If `v`
                             is None, it returns None. If `v` is invalid, it raises a
                             ValueError.
        serialization(cls, v): Converts a valid ObjectId `v` into a string for serialization.
                                If `v` is invalid, it raises a ValueError.
        __get_pydantic_core_schema__(cls, source_type, handler): Returns a schema for use
                                    with Pydantic, providing metadata about how to handle
                                    the serialization and validation of ObjectIds, ensuring
                                    that data adheres to the expected format both in Python
                                    and JSON.

    These methods are class methods, meaning they are called on the class rather than on
    instances of the class.
    """

    @classmethod
    def validate(cls, v, _: ValidationInfo):
        if v is None:
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("invalid Id")
        return str(v)

    # @classmethod
    # def serialization(cls, v):
    #     if not ObjectId.is_valid(v):
    #         raise ValueError("invalid Id")
    #     return str(v)

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
