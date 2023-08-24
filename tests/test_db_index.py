from pyodmongo import DbModel, Field
from pymongo import IndexModel
from typing import ClassVar


def test_index_unique_text_index():
    class MyClass(DbModel):
        attr_0: str
        attr_1: str = Field(index=True)
        attr_2: str = Field(unique=True)
        attr_3: str = Field(text_index=True)
        attr_4: str = Field(index=True, text_index=True)
        _collection: ClassVar = 'myclass'

    assert not MyClass.model_fields['attr_0']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_0']._attributes_set.get('unique') or False
    assert not MyClass.model_fields['attr_0']._attributes_set.get('text_index') or False

    assert MyClass.model_fields['attr_1']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_1']._attributes_set.get('unique') or False
    assert not MyClass.model_fields['attr_1']._attributes_set.get('text_index') or False

    assert not MyClass.model_fields['attr_2']._attributes_set.get('index') or False
    assert MyClass.model_fields['attr_2']._attributes_set.get('unique') or False
    assert not MyClass.model_fields['attr_2']._attributes_set.get('text_index') or False

    assert not MyClass.model_fields['attr_3']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_3']._attributes_set.get('unique') or False
    assert MyClass.model_fields['attr_3']._attributes_set.get('text_index') or False

    assert MyClass.model_fields['attr_4']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_4']._attributes_set.get('unique') or False
    assert MyClass.model_fields['attr_4']._attributes_set.get('text_index') or False


def test_check_index_field():
    class MyClass(DbModel):
        attr_1: str = Field(index=True)
        attr_2: str = Field(unique=True)
        attr_3: str = Field(text_index=True)
        attr_4: str = Field(index=True, text_index=True)
        _collection: ClassVar = 'myclass'

    assert hasattr(MyClass, '_indexes')
    assert len(MyClass._indexes) == 3
    assert all(type(item) is IndexModel for item in MyClass._indexes)
