from pyodmongo import DbModel, Field


class MyClass(DbModel):
    attr_legal: str = Field(
        default='PADRÃO', alias='attrLegal', index=True)


is_index = MyClass.model_fields['attr_legal']._attributes_set.get('index') or False
is_unique = MyClass.model_fields['attr_legal']._attributes_set.get('unique') or False
is_text_index = MyClass.model_fields['attr_legal']._attributes_set.get('text_index') or False

print(is_index, is_unique, is_text_index)
print(MyClass.model_fields['attr_legal'])
