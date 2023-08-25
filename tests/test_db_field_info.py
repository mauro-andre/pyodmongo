from pyodmongo import DbModel, Field, Id
from typing import ClassVar


def test_model_fiels_are_corrects():
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

    assert Lv1Filho.attr_lv1_one.field_name == 'attr_lv1_one'
    assert Lv1Filho.attr_lv1_one.field_alias == 'attrLv1One'
    assert Lv1.lv2.lv3.attr_lv3_one.field_name == 'attr_lv3_one'
    assert Lv1.lv2.lv3.attr_lv3_one.field_alias == 'attrLv3One'
    assert Lv1.lv2.lv3.attr_lv3_one.path_str == 'lv2.lv3Alias.attrLv3One'
    assert Lv1Filho.lv2.lv3.attr_lv3_one.path_str == 'lv2.lv3Alias.attrLv3One'
    assert Lv1.attr_lv1_two.field_type is str
    assert not Lv1.attr_lv1_two.by_reference
    assert not Lv1.attr_lv1_two.is_list
    assert not Lv1.attr_lv1_two.has_model_fields
