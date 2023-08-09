from fastapi import FastAPI
from pyodmondo_pv2 import Id, DbModel, DbField
from bson import ObjectId
from typing import ClassVar
from pydantic import Field

app = FastAPI()


class Lv3(DbModel):
    var3: str = 'Valor do Var1'
    _collection: ClassVar = 'tests_lv3'

class Lv2(DbModel):
    lv3: Lv3 = None
    var2: str = 'Valor do Var1'
    _collection: ClassVar = 'tests_lv2'
    
class Lv1(DbModel):
    var1: str = DbField(index=True, default='Vrau', alias='_var2', unique=True)
    test_id: Id = None
    test: Lv2 | Id = None
    test_dict: Lv2 = None
    test_list_reference: list[Lv2 | Id] = None
    test_list: list[Lv2] = None
    lv33: Lv3 = None
    _collection: ClassVar = 'tests_lv1'

@app.get('/')
async def test():
    obj_dict = {'_id': '64d19d2ea81f591eeb37823e', 'var': 'Shunda'}
    obj = Lv2(**obj_dict)
    print(Lv1.test_dict.var2)
    
    