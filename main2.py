from fastapi import FastAPI
from pyodmondo_pv2 import Id, DbModel, DbField, AsyncDbEngine, eq
from bson import ObjectId
from typing import ClassVar
from pydantic import Field

app = FastAPI()
db = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='PyODMongo')


class Lv3(DbModel):
    var3: str = DbField(default='Valor do Var33', index=True,  text_index=True)
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

lv3_1 = Lv3()
lv3_2 = Lv3(id='64d3e24c809e148e777e9f2b')
lv3_3 = Lv3(id='64d3e24c809e148e777e9f2c')

@app.get('/')
async def test():
    query = eq(Lv3.var3, 'Valor do Var3')
    return await db.find_one(Model=Lv3, query=query)
    # await db.save(lv3_1)
    
    
    