from pyodmongo import DbModel, Field, Id
from pydantic import BaseModel
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

    class Lv1Son(Lv1):
        lv1_son_attr: str

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

    obj_lv1_son = Lv1Son(id=id_5,
                         lv1_son_attr='value_lv1_son_attr',
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

    obj_lv1_son_expected_dict = {'_id': ObjectId('64e8fe13e6dcc2a63c365df8'),
                                 'attrLv1One': 'value_attr_lv1_one',
                                 'attr_lv1_two': 'value_attr_lv1_two',
                                 'created_at': None,
                                 'lv1_son_attr': 'value_lv1_son_attr',
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
    assert consolidate_dict(obj=obj_lv1_son, dct={}) == obj_lv1_son_expected_dict


def test_save_dict_with_basemodel_reference():
    class BaseModelClass(BaseModel):
        attr_bm: str

    class DbModelClass(DbModel):
        attr_dbm: str
        bm: BaseModelClass
        _collection: ClassVar = 'db_model_class'

    obj = DbModelClass(
        attr_dbm='attr_dbm',
        bm=BaseModelClass(attr_bm='attr_bm')
    )

    dct = consolidate_dict(obj=obj, dct={})
    assert dct == {'_id': None, 'created_at': None, 'updated_at': None, 'attr_dbm': 'attr_dbm', 'bm': {'attr_bm': 'attr_bm'}}


def test_field_with_union_more_than_two():
    class MyFirstClass(DbModel):
        attr_first: str = None
        _collection: ClassVar = 'my_first_class'

    class MyClass(DbModel):
        email: str = None
        mfc: list[MyFirstClass | Id] | None = None
        _collection: ClassVar = 'my_class'

    obj = MyClass(mfc=None)
    dct = consolidate_dict(obj=obj, dct={})
    assert dct == {'_id': None, 'created_at': None, 'updated_at': None, 'email': None, 'mfc': None}


def test_multiples_nested_references():
    class MyType1(BaseModel):
        attr_type_1: str = None

    class MyType2(BaseModel):
        attr_type_2: str = None

    class MyType3(BaseModel):
        attr_type_3: str = None

    class DbMyType(DbModel):
        attr_db: str = None
        my_type: MyType1 | MyType2 | MyType3 | None = None
        _collection: ClassVar = 'db_my_type'

    obj1 = DbMyType(my_type=MyType1())
    obj2 = DbMyType(my_type=MyType2())
    obj3 = DbMyType(my_type=MyType3())
    dct1 = {'_id': None,
            'attr_db': None,
            'created_at': None,
            'my_type': {'attr_type_1': None},
            'updated_at': None}
    dct2 = {'_id': None,
            'attr_db': None,
            'created_at': None,
            'my_type': {'attr_type_2': None},
            'updated_at': None}
    dct3 = {'_id': None,
            'attr_db': None,
            'created_at': None,
            'my_type': {'attr_type_3': None},
            'updated_at': None}

    assert consolidate_dict(obj=obj1, dct={}) == dct1
    assert consolidate_dict(obj=obj2, dct={}) == dct2
    assert consolidate_dict(obj=obj3, dct={}) == dct3


def test_list_of_ids_with_none():
    class MyType1(DbModel):
        attr_type_1: str = None
        _collection: ClassVar = 'my_type1'

    class DbMyType(DbModel):
        attr_db: str = None
        my_type: list[MyType1 | Id] = None
        _collection: ClassVar = 'db_my_type'

    obj = DbMyType()
    dct_expected = {'_id': None, 'created_at': None, 'updated_at': None, 'attr_db': None, 'my_type': None}
    assert consolidate_dict(obj=obj, dct={}) == dct_expected

    class DbMyType(DbModel):
        attr_db: str = None
        my_type: list[Id] = None
        _collection: ClassVar = 'db_my_type'

    obj = DbMyType()
    assert consolidate_dict(obj=obj, dct={}) == dct_expected
