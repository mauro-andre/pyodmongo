from pyodmongo import DbModel, Field, Id
from typing import ClassVar
from bson import ObjectId
from pyodmongo.queries import (eq, gt, gte, in_, lt, lte, ne, nin, text, and_, or_, mount_query_filter)
import pytest
from pprint import pprint


class Model1(DbModel):
    a: str = Field(alias='aAlias')
    b: str
    _collection: ClassVar = 'model_1'


class Model2(DbModel):
    c: str = Field(alias='cAlias')
    d: str
    e: Model1 = Field(alias='eAlias')
    _collection: ClassVar = 'model_2'


class Model3(DbModel):
    f: Model2
    g: Model2 | Id
    _collection: ClassVar = 'model_3'


def test_comparison_operators():

    assert eq(Model3.f.e.a, 'value').operator_dict() == {'f.eAlias.aAlias': {'$eq': 'value'}}
    assert gt(Model3.f.id, '64e8ef019af47dc6f91c5a48').operator_dict() == {'f._id': {'$gt': ObjectId('64e8ef019af47dc6f91c5a48')}}
    assert gt(Model3.f.e.id, '64e8ef019af47dc6f91c5a48').operator_dict() == {'f.eAlias._id': {'$gt': ObjectId('64e8ef019af47dc6f91c5a48')}}
    assert gte(Model3.g, '64e8ef019af47dc6f91c5a48').operator_dict() == {'g': {'$gte': ObjectId('64e8ef019af47dc6f91c5a48')}}
    assert in_(Model3.g, ['64e8ef019af47dc6f91c5a48', '64e8f1a5f1dae6703924546a']).operator_dict() == {'g': {'$in': [ObjectId('64e8ef019af47dc6f91c5a48'), ObjectId('64e8f1a5f1dae6703924546a')]}}
    assert nin(Model3.g.e.b, ['value_1', 'value_2']).operator_dict() == {'g.eAlias.b': {'$nin': ['value_1', 'value_2']}}
    assert text('Text to find').operator_dict() == {'$text': {'$search': '"Text to find"'}}


def test_logical_operators():
    op1 = eq(Model3.f.e.a, 'value')
    op2 = gt(Model3.f.id, '64e8ef019af47dc6f91c5a48')
    and_query = and_(op1, op2)
    or_query = or_(op1, op2)

    assert and_query.operator_dict() == {'$and': [{'f.eAlias.aAlias': {'$eq': 'value'}}, {'f._id': {'$gt': ObjectId('64e8ef019af47dc6f91c5a48')}}]}
    assert or_query.operator_dict() == {'$or': [{'f.eAlias.aAlias': {'$eq': 'value'}}, {'f._id': {'$gt': ObjectId('64e8ef019af47dc6f91c5a48')}}]}


def test_mount_query_filter_with_invalid_field():
    dict_input = {
        'c_eq': 'value1',
        'd_in': '["abc", "xyz"]',
        'vrau_eq': 'ddsff'
    }
    with pytest.raises(AttributeError):
        query = mount_query_filter(Model=Model2, items=dict_input, initial_comparison_operators=[])


def test_mount_query_filter():
    dict_input = {
        'id_eq': '64e8ef019af47dc6f91c5a48',
        'g_in': "['64e8ef019af47dc6f91c5a48', '64e8f1a5f1dae6703924546a']"
    }
    query = mount_query_filter(Model=Model3, items=dict_input, initial_comparison_operators=[])
    assert query.operator_dict() == {'$and': [{'_id': {'$eq': ObjectId('64e8ef019af47dc6f91c5a48')}},
                                              {'g': {'$in': [ObjectId('64e8ef019af47dc6f91c5a48'),
                                                             ObjectId('64e8f1a5f1dae6703924546a')]}}]}
