from typing import Any
from bson import Decimal128
from decimal import Decimal, Context, localcontext
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema, CoreSchema
from pydantic_core.core_schema import ValidationInfo, str_schema, float_schema


class DbDecimal(Decimal):
    def __new__(cls, value: Any, scale: None | int = None):
        if isinstance(value, Decimal128):
            value = value.to_decimal()
        elif isinstance(value, (int, float, str, Decimal)):
            _DEC128_CTX = Context(prec=34)
            with localcontext(_DEC128_CTX) as ctx:
                value = ctx.create_decimal(value)
            if scale:
                quantizer = Decimal("0." + ("0" * scale))
                value = value.quantize(quantizer)
        else:
            raise ValueError("Invalid decimal type")
        return super().__new__(cls, value)

    def to_scale(self, scale: int):
        quantizer = Decimal("0." + ("0" * scale))
        return self.quantize(quantizer)

    @classmethod
    def validate(cls, v, _: ValidationInfo):
        return cls(v)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:  # type: ignore
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=float_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: float(v) if isinstance(v, Decimal) else v, when_used="json"
            ),
        )
