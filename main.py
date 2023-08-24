from pyodmongo import DbModel, Field
from pymongo import IndexModel


class MyClass(DbModel):
    attr_legal: str = Field(default='PADRÃO', alias='attrLegal', index=True)
    attr_legal_2: str = Field(default='PADRÃO', alias='attrLegal', index=True)


print(type(MyClass._indexes[0]) is IndexModel)
