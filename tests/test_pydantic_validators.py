from pyodmongo import DbModel
from pydantic import BaseModel, field_validator, model_validator


def test_field_validator():
    class MyModel(DbModel):
        attr1: str
        attr2: str

        @field_validator('attr1')
        def validate_field(cls, value):
            return value + '_validate'

    obj = MyModel(attr1='value_1', attr2='value_2')
    print(obj)
