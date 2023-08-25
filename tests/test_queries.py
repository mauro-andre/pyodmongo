from pyodmongo import DbModel, Field, Id
from typing import ClassVar
from bson import ObjectId
from pyodmongo.queries import (eq, gt, gte, in_, lt, lte, ne, nin, text, and_, or_, mount_query_filter)


def test_comparison_operators():
    class Model1(DbModel):
        a: str = Field(alias='aAlias')
        b: str
        _collection: ClassVar = 'model_1'

    class Model2(DbModel):
        c: str = Field(alias='cAlias')
        d: str
        e: Model1 = Field(alias='eAlias')
        _collection: ClassVar = 'model_2'

    class Mode3(DbModel):
        f: Model2
        g: Model2 | Id
        _collection: ClassVar = 'model_3'

    assert eq(Mode3.f.e.a, 'value') == {'f.eAlias.aAlias': {'$eq': 'value'}}
    assert gt(Mode3.f.id, '64e8ef019af47dc6f91c5a48') == {'f._id': {'$gt': ObjectId('64e8ef019af47dc6f91c5a48')}}
    assert gt(Mode3.f.e.id, '64e8ef019af47dc6f91c5a48') == {'f.eAlias._id': {'$gt': ObjectId('64e8ef019af47dc6f91c5a48')}}
    assert gte(Mode3.g, '64e8ef019af47dc6f91c5a48') == {'g': {'$gte': ObjectId('64e8ef019af47dc6f91c5a48')}}
    assert in_(Mode3.g, ['64e8ef019af47dc6f91c5a48', '64e8f1a5f1dae6703924546a']) == {'g': {'$in': [ObjectId('64e8ef019af47dc6f91c5a48'), ObjectId('64e8f1a5f1dae6703924546a')]}}
    assert nin(Mode3.g.e.b, ['value_1', 'value_2']) == {'g.eAlias.b': {'$nin': ['value_1', 'value_2']}}
