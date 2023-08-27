from bson import ObjectId
from pyodmongo import DbModel, Field, Id, DbEngine, AsyncDbEngine
from pyodmongo.queries import eq, and_, or_
from pymongo import IndexModel
from typing import ClassVar
from pprint import pprint
import asyncio


mongo_uri = 'mongodb://localhost:27017/'
db_name = 'pyodmongo_tests'
db = DbEngine(mongo_uri=mongo_uri, db_name=db_name)
db_async = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name)


class Lv3(DbModel):
    attr_lv3_one: str = Field(alias='attrLv3One', index=True, text_index=True)
    attr_lv3_two: str = Field(text_index=True)
    _collection: ClassVar = 'lv3'


class Lv2(DbModel):
    attr_lv2_one: str = Field(alias='attrLv2One', index=True, unique=True)
    attr_lv2_two: str
    lv3: Lv3 | Id = Field(alias='lv3Alias')
    lv3_list: list[Id | Lv3]
    _collection: ClassVar = 'lv2'


class Lv1(DbModel):
    attr_lv1_one: str = Field(alias='attrLv1One')
    attr_lv1_two: str
    lv2: Lv2 | Id
    lv2_list: list[Lv2]
    lv2_list_ref: list[Id | Lv2]
    lv3_ref: Id | Lv3 = Field(alias='lv3Ref')
    lv3_list_ref: list[Lv3 | Id]
    _collection: ClassVar = 'lv1'


class Lv1Filho(Lv1):
    lv1_filho_attr: str


id_1 = '64e8fe13e6dcc2a63c365df4'
id_2 = '64e8fe13e6dcc2a63c365df5'
id_3 = '64e8fe13e6dcc2a63c365df6'
id_4 = '64e8fe13e6dcc2a63c365df7'
id_5 = '64e8fe13e6dcc2a63c365df8'

obj_lv3_1 = Lv3(
    attr_lv3_one='valor_attr_lv3_one',
    attr_lv3_two='valor_attr_lv3_two')

obj_lv3_2 = Lv3(id=id_2,
                attr_lv3_one='valor_attr_lv3_one',
                attr_lv3_two='valor_attr_lv3_two')

obj_lv_2_1 = Lv2(id=id_3, attr_lv2_one='valor_attr_lv2_one_1',
                 attr_lv2_two='valor_attr_lv2_two',
                 lv3=obj_lv3_1, lv3_list=[obj_lv3_1, obj_lv3_2])

obj_lv_2_2 = Lv2(id=id_4, attr_lv2_one='valor_attr_lv2_one_2',
                 attr_lv2_two='valor_attr_lv2_two',
                 lv3=obj_lv3_2, lv3_list=[obj_lv3_1, obj_lv3_2])

obj_lv1_filho = Lv1Filho(id=id_5,
                         lv1_filho_attr='value_lv1_filho_attr',
                         attr_lv1_one='value_attr_lv1_one',
                         attr_lv1_two='value_attr_lv1_two',
                         lv2=obj_lv_2_1,
                         lv2_list=[obj_lv_2_1, obj_lv_2_2],
                         lv2_list_ref=[obj_lv_2_1, obj_lv_2_2],
                         lv3_ref=obj_lv3_2,
                         lv3_list_ref=[obj_lv3_2, obj_lv3_1])

# db.save_all([obj_lv3_1, obj_lv3_2, obj_lv_2_1, obj_lv_2_2, obj_lv1_filho])
query = eq(Lv2.attr_lv2_one, 'valor_attr_lv2_one')
and_query = and_(
    eq(Lv3.attr_lv3_one, 'valor_attr_lv3_one'),
    eq(Lv3.attr_lv3_two, 'valor_attr_lv3_two')
)
result = db.save(obj_lv3_1)
print(result)
# find_result = db.save(obj_lv_2_2, raw_query={'vrau': 'vrou'})
# print(find_result)
# print(and_query.operator_dict())
# print(and_query)
# result = db.save(obj_lv3_1, query=query, raw_query={'vrau': 'vreu'})
# print(result)


async def main():
    await db_async.save_all([obj_lv3_1, obj_lv3_2, obj_lv_2_1, obj_lv_2_2])
# asyncio.run(main())

# query = eq(Lv2.id, '64e8fe13e6dcc2a63c365df6')
# obj = db.find_one(Model=Lv2, query=query, populate=True)
# print(obj)
# objs = db.find_many(Model=Lv2, populate=True)
# print(objs)

# {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
# {'n': 1, 'upserted': ObjectId('64ead6318257a081b9709d59'), 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}
