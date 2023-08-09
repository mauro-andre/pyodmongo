from fastapi import FastAPI
from pyodmongo.models import DbModel, Field, Id
from typing import ClassVar


app = FastAPI()

class Test(DbModel):
    var1: str = 'Valor do Var1'
    _collection: ClassVar = 'tests'
    
class TestMae(DbModel):
    var2: str = Field(index=True, default='Vrau', alias='_var2', unique=True)
    test_id: Id = None
    test: Test | Id = None
    test_dict: Test = None
    test_list_reference: list[Test | Id] = None
    test_list: list[Test] = None
    _collection: ClassVar = 'tests_maes'

@app.get('/')
async def test():
    obj_dict = {'_id': '64d19d2ea81f591eeb37823e', 'var': 'Shunda'}
    obj = Test(**obj_dict)
    print(TestMae.test_dict.var1)