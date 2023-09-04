from pyodmongo import DbModel
from pyodmongo.pydantic import field_validator, ConfigDict
from typing import ClassVar


def test_single_field_validator():
    class MyModel1(DbModel):
        attr1: str
        attr2: str
        model_config = ConfigDict()
        _collection: ClassVar = 'Vrau'

        @field_validator('attr2')
        def validate_attr2(cls, value):
            return value + '_mod'

    class MyModel2(MyModel1):
        attr3: str
        attr4: str

    obj = MyModel1(attr1='value_one', attr2='value_two')
    obj2 = MyModel2(attr1='value_one_one', attr2='value_two_two', attr3='value_three', attr4='value_four')

    assert obj.attr2 == 'value_two_mod'
    assert obj2.attr2 == 'value_two_two_mod'
