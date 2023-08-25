from pyodmongo import DbModel, Field, Id
from typing import ClassVar
from bson import ObjectId
from pyodmongo.engine.utils import consolidate_dict


def test_save_dict_is_correct():
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

    obj_lv3_1 = Lv3(id=id_1, attr_lv3_one='valor_attr_lv3_one',
                    attr_lv3_two='valor_attr_lv3_two')

    obj_lv3_2 = Lv3(id=id_2, attr_lv3_one='valor_attr_lv3_one',
                    attr_lv3_two='valor_attr_lv3_two')

    obj_lv_2_1 = Lv2(id=id_3, attr_lv2_one='valor_attr_lv2_one',
                     attr_lv2_two='valor_attr_lv2_two',
                     lv3=obj_lv3_1)

    obj_lv_2_2 = Lv2(id=id_4, attr_lv2_one='valor_attr_lv2_one',
                     attr_lv2_two='valor_attr_lv2_two',
                     lv3=obj_lv3_2)

    obj_lv1_filho = Lv1Filho(id=id_5,
                             lv1_filho_attr='value_lv1_filho_attr',
                             attr_lv1_one='value_attr_lv1_one',
                             attr_lv1_two='value_attr_lv1_two',
                             lv2=obj_lv_2_1,
                             lv2_list=[obj_lv_2_1, obj_lv_2_2],
                             lv2_list_ref=[obj_lv_2_1, obj_lv_2_2],
                             lv3_ref=obj_lv3_2,
                             lv3_list_ref=[obj_lv3_2, obj_lv3_1])

    obj_lv3_1_expected_dict = {'_id': ObjectId('64e8fe13e6dcc2a63c365df4'),
                               'attrLv3One': 'valor_attr_lv3_one',
                               'attr_lv3_two': 'valor_attr_lv3_two',
                               'created_at': None,
                               'updated_at': None}

    obj_lv_2_1_expected_dict = {'_id': ObjectId('64e8fe13e6dcc2a63c365df6'),
                                'attrLv2One': 'valor_attr_lv2_one',
                                'attr_lv2_two': 'valor_attr_lv2_two',
                                'created_at': None,
                                'lv3Alias': ObjectId('64e8fe13e6dcc2a63c365df4'),
                                'updated_at': None}

    obj_lv1_filho_expected_dict = {'_id': ObjectId('64e8fe13e6dcc2a63c365df8'),
                                   'attrLv1One': 'value_attr_lv1_one',
                                   'attr_lv1_two': 'value_attr_lv1_two',
                                   'created_at': None,
                                   'lv1_filho_attr': 'value_lv1_filho_attr',
                                   'lv2': ObjectId('64e8fe13e6dcc2a63c365df6'),
                                   'lv2_list': [{'_id': ObjectId('64e8fe13e6dcc2a63c365df6'),
                                                 'attrLv2One': 'valor_attr_lv2_one',
                                                 'attr_lv2_two': 'valor_attr_lv2_two',
                                                 'created_at': None,
                                                 'lv3Alias': ObjectId('64e8fe13e6dcc2a63c365df4'),
                                                 'updated_at': None},
                                                {'_id': ObjectId('64e8fe13e6dcc2a63c365df7'),
                                                 'attrLv2One': 'valor_attr_lv2_one',
                                                 'attr_lv2_two': 'valor_attr_lv2_two',
                                                 'created_at': None,
                                                 'lv3Alias': ObjectId('64e8fe13e6dcc2a63c365df5'),
                                                 'updated_at': None}],
                                   'lv2_list_ref': [ObjectId('64e8fe13e6dcc2a63c365df6'),
                                                    ObjectId('64e8fe13e6dcc2a63c365df7')],
                                   'lv3Ref': ObjectId('64e8fe13e6dcc2a63c365df5'),
                                   'lv3_list_ref': [ObjectId('64e8fe13e6dcc2a63c365df5'),
                                                    ObjectId('64e8fe13e6dcc2a63c365df4')],
                                   'updated_at': None}

    assert consolidate_dict(obj=obj_lv3_1, dct={}) == obj_lv3_1_expected_dict
    assert consolidate_dict(obj=obj_lv_2_1, dct={}) == obj_lv_2_1_expected_dict
    assert consolidate_dict(obj=obj_lv1_filho, dct={}) == obj_lv1_filho_expected_dict
