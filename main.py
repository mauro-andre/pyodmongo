from bson import ObjectId
from pprint import pprint
from db.crud import save, find_one, find_many
from db.models import DbModel, Id
from fastapi import FastAPI
from pydantic import Field
from typing import ClassVar

app = FastAPI()


class Lv8(DbModel):
    var_8_1: str
    var_8_2: str
    _collection: ClassVar = 'Lv8'


class Lv7(DbModel):
    var_7: str
    lv_8: Lv8 | Id
    _collection: ClassVar = 'Lv7'


class Lv6(DbModel):
    var6: str
    lv_7: list[Lv7 | Id]
    _collection: ClassVar = 'Lv6'


class Lv5(DbModel):
    var5: str
    lv_6: Lv6 | Id
    _collection: ClassVar = 'Lv5'


class Lv4(DbModel):
    var4: str
    lv_5: Lv5 | Id
    _collection: ClassVar = 'Lv4'


class Lv3(DbModel):
    var3: str
    lv_4: list[Lv4 | Id]
    _collection: ClassVar = 'Lv3'


class Lv2(DbModel):
    var2: str
    lv_3: Lv3 | Id
    _collection: ClassVar = 'Lv2'


class Lv1(DbModel):
    var1: str
    lv_2: Lv2
    _collection: ClassVar = 'Lv1'

# 64b2e3ec0bff1e48346f6fa4
# 64b2ece08c9ce793f4841a00
# 64b2e3ec0bff1e48346f6fa5
# 64b2e3ec0bff1e48346f6fa6
# 64b2e3ec0bff1e48346f6fa7
# 64b2e3ec0bff1e48346f6fa8
# 64b2ece08c9ce793f4841a01
# 64b2e3ec0bff1e48346f6fa9
# 64b2e3ec0bff1e48346f6faa
# 64b2e3ec0bff1e48346f6fab
# 64b2e3ec0bff1e48346f6fac
# 64b2e3ec0bff1e48346f6fad
# 64b300b7c3b263e9907f3783
# 64b300b7c3b263e9907f3784
# 64b300b7c3b263e9907f3785
# 64b300b7c3b263e9907f3786
# 64b300b7c3b263e9907f3787
# 64b300b7c3b263e9907f3788
# 64b300b7c3b263e9907f3789
# 64b300b7c3b263e9907f378a


@app.get('/test')
async def test(id: str, docs_per_page: int, current_page: int = 1):
    # return await find_one(Model=Lv1, query={'_id': ObjectId(id)})
    return await find_many(Model=Lv1,
                           query={'_id': ObjectId(id)},
                           current_page=current_page,
                           docs_per_page=docs_per_page,
                           )
    # print(Lv2.lv_3)
    # lv_8_1 = Lv8(id='64b2e3ec0bff1e48346f6fa4',
    #              var_8_1='var_8_1', var_8_2='var_8_1')
    # lv_8_2 = Lv8(id='64b2ece08c9ce793f4841a00',
    #              var_8_1='var_8_2', var_8_2='var_8_2')
    # lv_8_3 = Lv8(id='64b300b7c3b263e9907f378a',
    #              var_8_1='var_8_3', var_8_2='var_8_3')
    # lv_8_4 = Lv8(id='64b300b7c3b263e9907f3789',
    #              var_8_1='var_8_4', var_8_2='var_8_4')

    # lv_7_1 = [
    #     Lv7(id='64b2e3ec0bff1e48346f6fa5', var_7='var_7_1', lv_8=lv_8_1),
    #     Lv7(id='64b2e3ec0bff1e48346f6fa6', var_7='var_7_2', lv_8=lv_8_2),
    # ]
    # lv_7_2 = [
    #     Lv7(id='64b300b7c3b263e9907f3788', var_7='var_7_3', lv_8=lv_8_3),
    #     Lv7(id='64b300b7c3b263e9907f3787', var_7='var_7_4', lv_8=lv_8_4),
    # ]

    # lv_6_1 = Lv6(id='64b2e3ec0bff1e48346f6fa7', var6='var_6_1', lv_7=lv_7_1)
    # lv_6_2 = Lv6(id='64b300b7c3b263e9907f3786', var6='var_6_2', lv_7=lv_7_2)

    # lv_5_1 = Lv5(id='64b2e3ec0bff1e48346f6fa8', var5='var_5_1', lv_6=lv_6_1)
    # lv_5_2 = Lv5(id='64b2ece08c9ce793f4841a01', var5='var_5_2', lv_6=lv_6_2)

    # lv_4 = [
    #     Lv4(id='64b2e3ec0bff1e48346f6fa9', var4='var_4_1', lv_5=lv_5_1),
    #     Lv4(id='64b2e3ec0bff1e48346f6faa', var4='var_4_2', lv_5=lv_5_2)
    # ]

    # lv_3 = Lv3(id='64b2e3ec0bff1e48346f6fab', var3='var_3', lv_4=lv_4)

    # lv_2 = Lv2(id='64b2e3ec0bff1e48346f6fac', var2='var_2', lv_3=lv_3)

    # lv_1 = Lv1(id='64b2e3ec0bff1e48346f6fad', var1='var_1', lv_2=lv_2)
    # await save(lv_8_1)
    # await save(lv_8_2)
    # await save(lv_8_3)
    # await save(lv_8_4)
    # await save(lv_7_1[0])
    # await save(lv_7_1[1])
    # await save(lv_7_2[0])
    # await save(lv_7_2[1])
    # await save(lv_6_1)
    # await save(lv_6_2)
    # await save(lv_5_1)
    # await save(lv_5_2)
    # await save(lv_4[0])
    # await save(lv_4[1])
    # await save(lv_3)
    # await save(lv_2)
    # await save(lv_1)

    pass
