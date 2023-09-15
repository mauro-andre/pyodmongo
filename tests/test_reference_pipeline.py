from pyodmongo import DbModel, Id, Field
from pydantic import BaseModel
from typing import ClassVar


def test_if_reference_pipeline_is_correct():
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

    expected = [{'$lookup': {'as': 'lv2',
                             'foreignField': '_id',
                             'from': 'lv2',
                             'localField': 'lv2'}},
                {'$set': {'lv2': {'$arrayElemAt': ['$lv2', 0]}}},
                {'$lookup': {'as': 'lv2.lv3Alias',
                             'foreignField': '_id',
                             'from': 'lv3',
                             'localField': 'lv2.lv3Alias'}},
                {'$set': {'lv2.lv3Alias': {'$arrayElemAt': ['$lv2.lv3Alias', 0]}}},
                {'$lookup': {'as': 'lv3_list_multi',
                             'foreignField': '_id',
                             'from': 'lv2',
                             'localField': 'lv3_list_multi'}},
                {'$lookup': {'as': 'lv2Ref',
                             'foreignField': '_id',
                             'from': 'lv3',
                             'localField': 'lv2Ref'}},
                {'$set': {'lv2Ref': {'$arrayElemAt': ['$lv2Ref', 0]}}},
                {'$lookup': {'as': 'lv3_list_ref',
                             'foreignField': '_id',
                             'from': 'lv3',
                             'localField': 'lv3_list_ref'}}]
    assert Lv1Filho._reference_pipeline == expected


def test_field_with_union_more_than_two():
    class MyFirstClass(DbModel):
        attr_first: str = None
        _collection: ClassVar = 'my_first_class'

    class MyClass(DbModel):
        email: str = None
        mfc0: Id = None
        mfc1: MyFirstClass | None | Id = None
        mfc2: None | MyFirstClass | Id = None
        mfc3: None | Id | MyFirstClass = None
        mfc4: MyFirstClass | Id | None = None
        mfc5: Id | MyFirstClass | None = None
        mfc6: Id | None | MyFirstClass = None
        mfc7: list[Id | None | MyFirstClass] = None
        mfc8: list[Id | MyFirstClass | None] | None = None
        mfc9: None | list[MyFirstClass | None | Id] = None
        _collection: ClassVar = 'my_class'

    assert MyClass._reference_pipeline == [{'$lookup': {'as': 'mfc1',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc1'}},
                                           {'$set': {'mfc1': {'$arrayElemAt': ['$mfc1', 0]}}},
                                           {'$lookup': {'as': 'mfc2',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc2'}},
                                           {'$set': {'mfc2': {'$arrayElemAt': ['$mfc2', 0]}}},
                                           {'$lookup': {'as': 'mfc3',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc3'}},
                                           {'$set': {'mfc3': {'$arrayElemAt': ['$mfc3', 0]}}},
                                           {'$lookup': {'as': 'mfc4',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc4'}},
                                           {'$set': {'mfc4': {'$arrayElemAt': ['$mfc4', 0]}}},
                                           {'$lookup': {'as': 'mfc5',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc5'}},
                                           {'$set': {'mfc5': {'$arrayElemAt': ['$mfc5', 0]}}},
                                           {'$lookup': {'as': 'mfc6',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc6'}},
                                           {'$set': {'mfc6': {'$arrayElemAt': ['$mfc6', 0]}}},
                                           {'$lookup': {'as': 'mfc7',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc7'}},
                                           {'$lookup': {'as': 'mfc8',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc8'}},
                                           {'$lookup': {'as': 'mfc9',
                                                        'foreignField': '_id',
                                                        'from': 'my_first_class',
                                                        'localField': 'mfc9'}}]


def test_multiples_nested_references():
    class MyType1(BaseModel):
        attr_type_1: str = None

    class MyType2(BaseModel):
        attr_type_2: str = None

    class MyType3(BaseModel):
        attr_type_3: str = None

    class MyType4(DbModel):
        attr_type_4: str = None
        _collection: ClassVar = 'my_type_4'

    class DbMyType(DbModel):
        attr_db: str = None
        my_type: MyType1 | MyType2 | MyType3 | None = None
        my_type_4: MyType4 | Id = None
        _collection: ClassVar = 'db_my_type'

    assert DbMyType._reference_pipeline == [{'$lookup': {'as': 'my_type_4',
                                                         'foreignField': '_id',
                                                         'from': 'my_type_4',
                                                         'localField': 'my_type_4'}},
                                            {'$set': {'my_type_4': {'$arrayElemAt': ['$my_type_4', 0]}}}]


def test_manual_pipeline():
    class MyModel1(DbModel):
        attr1: str
        _collection: ClassVar = 'my_model_1'

    class MyModel2(DbModel):
        attr2: str
        my_model_1: MyModel1
        _collection: ClassVar = 'my_model_2'
        _pipeline: ClassVar = ['manual pipeline here']

    assert MyModel1._pipeline == []
    assert MyModel2._pipeline == ['manual pipeline here']
