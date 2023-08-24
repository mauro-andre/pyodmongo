from pyodmongo import DbModel, Field


def test_index_unique_text_index():
    class MyClass(DbModel):
        attr_1: str = Field(index=True)
        attr_2: str = Field(unique=True)
        attr_3: str = Field(text_index=True)

    assert MyClass.model_fields['attr_1']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_1']._attributes_set.get('unique') or False
    assert not MyClass.model_fields['attr_1']._attributes_set.get('text_index') or False
    assert not MyClass.model_fields['attr_2']._attributes_set.get('index') or False
    assert MyClass.model_fields['attr_2']._attributes_set.get('unique') or False
    assert not MyClass.model_fields['attr_2']._attributes_set.get('text_index') or False
    assert not MyClass.model_fields['attr_3']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_3']._attributes_set.get('unique') or False
    assert MyClass.model_fields['attr_3']._attributes_set.get('text_index') or False
