from fastapi import FastAPI, Request
from pyodmondo_pv2 import Id, DbModel, DbField, AsyncDbEngine, DbEngine
from pyodmondo_pv2.queries import eq, in_, mount_query_filter, nin
from bson import ObjectId
from typing import ClassVar
from pydantic import Field
from pprint import pprint

app = FastAPI()
db = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='PyODMongo')


class Lv3(DbModel):
    var31: str = DbField(default='Valor do Var33', index=True,  text_index=True)
    var32: str = DbField(default='Valor do Var32', text_index=True)
    _collection: ClassVar = 'tests_lv3'

class Lv2(DbModel):
    var2: str = DbField(default='Valor do Var2', index=True,  text_index=True)
    lv3: Lv3 | Id
    _collection: ClassVar = 'tests_lv2'
    
class Lv1(DbModel):
    var1: str = DbField(default='Valor do Var1', index=True,  text_index=True)
    lv2: Lv2 | Id
    lv3_list: list[Lv3 | Id]
    _collection: ClassVar = 'tests_lv1'

# 64d3e24c809e148e777e9f2a
# 64d3e24c809e148e777e9f2b
# 64d3e24c809e148e777e9f2c
# 64d3e24c809e148e777e9f2d
# 64d3e24c809e148e777e9f2e
# 64d3e24c809e148e777e9f2f

lv3_1 = Lv3(id='64d3e24c809e148e777e9f2a')
lv3_2 = Lv3(id='64d3e24c809e148e777e9f2b')
lv3_3 = Lv3(id='64d3e24c809e148e777e9f2c')
lv2_1 = Lv2(id='64d3e24c809e148e777e9f2d', lv3=lv3_1)
lv1_1 = Lv1(id='64d3e24c809e148e777e9f2e', lv2=lv2_1, lv3_list=[lv3_2, lv3_3])

# save_result =  db.save_all([lv3_1, lv3_2, lv3_3, lv2_1, lv1_1])
# print(save_result)

# print(db.find_one(Model=Lv1, query={}))

@app.get('/')
def test(request: Request):
    # x = db.
    vrau =  db.find_one(Model=Lv1, query=eq(Lv1.id, '64d3e24c809e148e777e9f2e'))
    print(vrau)
    # save_result =  await db.save_all([lv3_1, lv3_2, lv3_3, lv2_1, lv1_1])
    # print(save_result)
    # print(type(request.query_params))
    # print(type({'var2': 'valor1', 'var3': 'valor3'}))
    # query = mount_query_filter(items=request.query_params, Model=Lv3, operators=[])
    # pprint(query)
    # return await db.find_many(Model=Lv3, query={}, current_page=1, docs_per_page=1000)
    # return await db.delete_one(Model=Lv3, query=query)
    # await db.save(lv3_1)
    
    
    