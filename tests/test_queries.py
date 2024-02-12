from pyodmongo import DbModel, Field, Id
from pydantic import BaseModel
from typing import ClassVar
from bson import ObjectId
from pyodmongo.queries import (
    eq,
    gt,
    gte,
    in_,
    lt,
    lte,
    ne,
    nin,
    text,
    and_,
    or_,
    nor,
    mount_query_filter,
)
from pyodmongo.services.query_operators import query_dict
import pytest


class Model1(DbModel):
    a: str = Field(alias="aAlias")
    b: str
    _collection: ClassVar = "model_1"


class Model2(DbModel):
    c: str = Field(alias="cAlias")
    d: str
    e: Model1 = Field(alias="eAlias")
    _collection: ClassVar = "model_2"


class Model3(DbModel):
    f: Model2
    g: Model2 | Id
    _collection: ClassVar = "model_3"


def test_comparison_operators():
    assert query_dict(query_operator=eq(Model3.f.e.a, "value"), dct={}) == {
        "f.eAlias.aAlias": {"$eq": "value"}
    }
    assert query_dict(
        query_operator=gt(Model3.f.id, "64e8ef019af47dc6f91c5a48"), dct={}
    ) == {"f._id": {"$gt": ObjectId("64e8ef019af47dc6f91c5a48")}}
    assert query_dict(
        query_operator=gt(Model3.f.e.id, "64e8ef019af47dc6f91c5a48"), dct={}
    ) == {"f.eAlias._id": {"$gt": ObjectId("64e8ef019af47dc6f91c5a48")}}
    assert query_dict(
        query_operator=gte(Model3.g, "64e8ef019af47dc6f91c5a48"), dct={}
    ) == {"g": {"$gte": ObjectId("64e8ef019af47dc6f91c5a48")}}
    assert query_dict(
        query_operator=in_(
            Model3.g, ["64e8ef019af47dc6f91c5a48", "64e8f1a5f1dae6703924546a"]
        ),
        dct={},
    ) == {
        "g": {
            "$in": [
                ObjectId("64e8ef019af47dc6f91c5a48"),
                ObjectId("64e8f1a5f1dae6703924546a"),
            ]
        }
    }
    assert query_dict(
        query_operator=nin(Model3.g.e.b, ["value_1", "value_2"]), dct={}
    ) == {"g.eAlias.b": {"$nin": ["value_1", "value_2"]}}
    assert query_dict(query_operator=text("Text to find"), dct={}) == {
        "$text": {"$search": '"Text to find"'}
    }
    assert query_dict(query_operator=lt(Model2.d, "value_d"), dct={}) == {
        "d": {"$lt": "value_d"}
    }
    assert query_dict(query_operator=lte(Model2.c, "value_c"), dct={}) == {
        "cAlias": {"$lte": "value_c"}
    }
    assert query_dict(query_operator=ne(Model3.g.e.a, "value_a"), dct={}) == {
        "g.eAlias.aAlias": {"$ne": "value_a"}
    }


def test_logical_operators():
    op1 = eq(Model3.f.e.a, "value")
    op2 = gt(Model3.f.id, "64e8ef019af47dc6f91c5a48")
    and_query = and_(op1, op2)
    or_query = or_(op1, op2)
    nor_query = nor(op1, op2)

    assert query_dict(query_operator=and_query, dct={}) == {
        "$and": [
            {"f.eAlias.aAlias": {"$eq": "value"}},
            {"f._id": {"$gt": ObjectId("64e8ef019af47dc6f91c5a48")}},
        ]
    }
    assert query_dict(query_operator=or_query, dct={}) == {
        "$or": [
            {"f.eAlias.aAlias": {"$eq": "value"}},
            {"f._id": {"$gt": ObjectId("64e8ef019af47dc6f91c5a48")}},
        ]
    }
    assert query_dict(query_operator=nor_query, dct={}) == {
        "$nor": [
            {"f.eAlias.aAlias": {"$eq": "value"}},
            {"f._id": {"$gt": ObjectId("64e8ef019af47dc6f91c5a48")}},
        ]
    }


def test_mount_query_filter_with_invalid_field():
    dict_input = {"c_eq": "value1", "d_in": '["abc", "xyz"]', "vrau_eq": "ddsff"}
    with pytest.raises(AttributeError):
        query = mount_query_filter(
            Model=Model2, items=dict_input, initial_comparison_operators=[]
        )


def test_mount_query_filter():
    dict_input = {
        "id_eq": "64e8ef019af47dc6f91c5a48",
        "g_in": "['64e8ef019af47dc6f91c5a48', '64e8f1a5f1dae6703924546a']",
    }
    query = mount_query_filter(
        Model=Model3, items=dict_input, initial_comparison_operators=[]
    )
    assert query_dict(query_operator=query, dct={}) == {
        "$and": [
            {"_id": {"$eq": ObjectId("64e8ef019af47dc6f91c5a48")}},
            {
                "g": {
                    "$in": [
                        ObjectId("64e8ef019af47dc6f91c5a48"),
                        ObjectId("64e8f1a5f1dae6703924546a"),
                    ]
                }
            },
        ]
    }


def test_mount_query_filter_inheritance():
    class MainModel(DbModel):
        attr_1: str = None
        _collection: ClassVar = "main_model"

    class SecondModel(MainModel):
        attr_2: str = None

    class ThirdModel(SecondModel):
        attr_3: str = None

    class FourthModel(ThirdModel, SecondModel):
        attr_4: str = None

    input_dict = {
        "attr_1_eq": "Value1",
        "attr_2_eq": "Value2",
        "attr_3_eq": "Value3",
        "attr_4_eq": "Value4",
        "attr_4_in": "",
        "attr_4_er": "Value_error",
    }
    query = mount_query_filter(
        Model=FourthModel, items=input_dict, initial_comparison_operators=[]
    )
    expected_query_dict = {
        "$and": [
            {"attr_1": {"$eq": "Value1"}},
            {"attr_2": {"$eq": "Value2"}},
            {"attr_3": {"$eq": "Value3"}},
            {"attr_4": {"$eq": "Value4"}},
        ]
    }

    assert query_dict(query_operator=query, dct={}) == expected_query_dict


def test_mount_query_filter_is_not_inheritance():
    class MainModel(BaseModel):
        attr_1: str = None
        _collection: ClassVar = "main_model"

    class SecondModel(MainModel):
        attr_2: str = None

    class ThirdModel(SecondModel):
        attr_3: str = None

    class FourthModel(ThirdModel, SecondModel):
        attr_4: str = None

    input_dict = {
        "attr_1_eq": "Value1",
        "attr_2_eq": "Value2",
        "attr_3_eq": "Value3",
        "attr_4_eq": "Value4",
    }
    with pytest.raises(TypeError, match="Model must be a DbModel"):
        query = mount_query_filter(
            Model=FourthModel, items=input_dict, initial_comparison_operators=[]
        )


def test_mount_query_filter_with_none_value():
    class MainModel(DbModel):
        attr_1: str = None
        _collection: ClassVar = "main_model"

    input_dict = {}
    query = mount_query_filter(
        Model=MainModel, items=input_dict, initial_comparison_operators=[]
    )
    assert query is None


def test_mount_query_filter_with_regex():
    import re

    class MyModel(DbModel):
        attr1: str
        attr2: str

    input_dict = {"attr1_in": "['/^agr[oóôõ]s/i', 123, 'abc']", "attr2_eq": "123"}

    query = mount_query_filter(
        Model=MyModel, items=input_dict, initial_comparison_operators=[]
    )
    query_dct = query_dict(query_operator=query, dct={})
    assert query_dct == {
        "$and": [
            {"attr1": {"$in": [re.compile("^agr[oóôõ]s", re.IGNORECASE), 123, "abc"]}},
            {"attr2": {"$eq": 123}},
        ]
    }


def test_logical_operator_inside_another():
    query = and_(
        or_(
            eq(Model1.a, "string_to_find_2"),
            eq(Model1.a, "string_to_find_3"),
            and_(gt(Model1.b, "value_b"), gt(Model1.b, "value_c")),
        ),
        eq(Model1.a, "string_to_find_1"),
    )
    expected_dct = {
        "$and": [
            {
                "$or": [
                    {"aAlias": {"$eq": "string_to_find_2"}},
                    {"aAlias": {"$eq": "string_to_find_3"}},
                    {"$and": [{"b": {"$gt": "value_b"}}, {"b": {"$gt": "value_c"}}]},
                ]
            },
            {"aAlias": {"$eq": "string_to_find_1"}},
        ]
    }
    query_dct = query_dict(query_operator=query, dct={})
    assert query_dct == expected_dct
