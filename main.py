from pyodmongo import DbModel, Field, Id
from pymongo import IndexModel
from typing import ClassVar
from pprint import pprint


class Lv3(DbModel):
    attr_lv3_one: str = Field(alias='attrLv3One')
    attr_lv3_two: str
    _collection: ClassVar = 'lv3'


class Lv2(DbModel):
    attr_lv2_one: str = Field(alias='attrLv2One')
    attr_lv2_two: str
    lv3: Lv3 | Id = Field(alias='lv3Alias')
    _collection: ClassVar = 'lv2'


class Lv1(DbModel):
    attr_lv1_one: str = Field(alias='attrLv1One')
    attr_lv1_two: str
    lv2: Lv2 | Id
    lv2_list: list[Lv2]
    lv3_list_multi: list[Id | Lv2]
    lv2_ref: Id | Lv3 = Field(alias='lv2Ref')
    lv3_list_ref: list[Lv3 | Id]
    _collection: ClassVar = 'lv1'


class Lv1Filho(Lv1):
    lv1_filho_attr: str


pprint(Lv1Filho._reference_pipeline)
