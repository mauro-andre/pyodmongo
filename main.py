from pyodmongo import DbModel, Field, Id
from pymongo import IndexModel


class Lv3(DbModel):
    attr_lv3_one: str = Field(alias='attrLv3One')
    attr_lv3_two: str


class Lv2(DbModel):
    attr_lv2_one: str = Field(alias='attrLv2One')
    attr_lv2_two: str


class Lv1(DbModel):
    attr_lv1_one: str = Field(alias='attrLv1One')
    attr_lv1_two: str
    lv2: Lv2
    lv_list: list[Lv2]
    lv_list_multi: list[Lv3 | Lv2]
    lv2_ref: Id | Lv2
    lv2_list_ref: list[Lv3 | Id]
