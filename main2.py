from bson import ObjectId
from pprint import pprint
from db_model import save, find_one, DbModel, Id
from fastapi import FastAPI
from pydantic import Field
from typing import ClassVar

app = FastAPI()


class Lv3(DbModel):
    var_3: str
    _collection: ClassVar = 'Lv3'


class Lv21(DbModel):
    var_21: str
    var_3: Lv3 | Id
    _collection: ClassVar = 'Lv21'


class Lv22(DbModel):
    var_22: str
    var_3: list[Lv3 | Id]
    _collection: ClassVar = 'Lv22'


class Lv1(DbModel):
    var_1_1: str
    var_1_2: Lv21 | Id
    var_1_3: list[Lv22 | Id]
    _collection: ClassVar = 'Lv1'


id_3_1 = '64b57354374aac33adfb4ed2'
id_3_2 = '64b57354374aac33adfb4ed3'
id_3_3 = '64b57354374aac33adfb4ed4'
id_21_1 = '64b57354374aac33adfb4ed5'
id_22_1 = '64b57354374aac33adfb4ed6'
id_22_2 = '64b57354374aac33adfb4ed7'
id_1 = '64b57354374aac33adfb4ed8'
# 64b57354374aac33adfb4ed9
# 64b57354374aac33adfb4eda
# 64b57354374aac33adfb4edb
# 64b57354374aac33adfb4edc
# 64b57354374aac33adfb4edd


@app.get('/test')
async def teste():
    lv_3_1 = Lv3(id=id_3_1, var_3='LV_3_1')
    lv_3_2 = Lv3(id=id_3_2, var_3='LV_3_2')
    lv_3_3 = Lv3(id=id_3_3, var_3='LV_3_3')
    lv_21_1 = Lv21(id=id_21_1, var_21='var_21_1', var_3=lv_3_1)
    lv_22_1 = Lv22(id=id_22_1, var_22='var_22_1', var_3=[lv_3_2, lv_3_3])
    lv_22_2 = Lv22(id=id_22_2, var_22='var_22_2', var_3=[lv_3_3, lv_3_2])
    lv_1 = Lv1(id=id_1, var_1_1='var_1_1',
               var_1_2=lv_21_1, var_1_3=[lv_22_1, lv_22_2])
    # await save(lv_3_1)
    # await save(lv_3_2)
    # await save(lv_3_2)
    # await save(lv_21_1)
    # await save(lv_22_1)
    # await save(lv_22_2)
    # await save(lv_1)
    lv_1_load: Lv1 = await find_one(Model=Lv1, query={'_id': ObjectId('64b57354374aac33adfb4ed8')})
    print(lv_1_load.__fields__)
    # return lv_1_load
    pass
