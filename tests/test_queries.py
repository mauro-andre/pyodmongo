from pyodmongo import DbModel, Field, Id
from pydantic import BaseModel
from typing import ClassVar
from bson import ObjectId
from datetime import datetime
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
    sort,
    mount_query_filter,
)
from pyodmongo.services.query_operators import query_dict, sort_dict
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
        query, _ = mount_query_filter(
            Model=Model2, items=dict_input, initial_comparison_operators=[]
        )


def test_mount_query_filter():
    dict_input = {
        "id_eq": "64e8ef019af47dc6f91c5a48",
        "g_in": "['64e8ef019af47dc6f91c5a48', '64e8f1a5f1dae6703924546a']",
    }
    query, _ = mount_query_filter(
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
    query, _ = mount_query_filter(
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
        query, _ = mount_query_filter(
            Model=FourthModel, items=input_dict, initial_comparison_operators=[]
        )


def test_mount_query_filter_with_none_value():
    class MainModel(DbModel):
        attr_1: str = None
        _collection: ClassVar = "main_model"

    input_dict = {}
    query, _ = mount_query_filter(
        Model=MainModel, items=input_dict, initial_comparison_operators=[]
    )
    assert query is None


def test_mount_query_filter_with_regex():
    import re

    class MyModel(DbModel):
        attr1: str
        attr2: str

    input_dict_1 = {"attr1_in": "['/^agr[oóôõ]s/i', 123, 'abc']", "attr2_eq": "123"}
    input_dict_2 = {"attr1_in": "['/^agr[oóôõ]s/m', 123, 'abc']", "attr2_eq": "123"}
    input_dict_3 = {"attr1_in": "['/^agr[oóôõ]s/s', 123, 'abc']", "attr2_eq": "123"}

    query_1, _ = mount_query_filter(
        Model=MyModel, items=input_dict_1, initial_comparison_operators=[]
    )
    query_2, _ = mount_query_filter(
        Model=MyModel, items=input_dict_2, initial_comparison_operators=[]
    )
    query_3, _ = mount_query_filter(
        Model=MyModel, items=input_dict_3, initial_comparison_operators=[]
    )
    query_dct_1 = query_dict(query_operator=query_1, dct={})
    query_dct_2 = query_dict(query_operator=query_2, dct={})
    query_dct_3 = query_dict(query_operator=query_3, dct={})
    assert query_dct_1 == {
        "$and": [
            {"attr1": {"$in": [re.compile("^agr[oóôõ]s", re.IGNORECASE), 123, "abc"]}},
            {"attr2": {"$eq": 123}},
        ]
    }
    assert query_dct_2 == {
        "$and": [
            {"attr1": {"$in": [re.compile("^agr[oóôõ]s", re.MULTILINE), 123, "abc"]}},
            {"attr2": {"$eq": 123}},
        ]
    }
    assert query_dct_3 == {
        "$and": [
            {"attr1": {"$in": [re.compile("^agr[oóôõ]s", re.DOTALL), 123, "abc"]}},
            {"attr2": {"$eq": 123}},
        ]
    }


def test_mount_query_filter_with_data_types():
    class MyClass(DbModel):
        string_value: str
        int_value: int
        float_value: float
        bool_value: bool
        date_value: datetime
        _collection: ClassVar = "my_class"

    input_dct = {
        "string_value_eq": "AString",
        "int_value_gt": "10",
        "float_value_lte": "50.6",
        "bool_value_eq": "True",
        "date_value_lte": "2024-06-01",
    }
    query_dct, _ = mount_query_filter(
        Model=MyClass, items=input_dct, initial_comparison_operators=[]
    )
    assert query_dct.operators[0].value == "AString"
    assert type(query_dct.operators[0].value) is str
    assert query_dct.operators[1].value == 10
    assert type(query_dct.operators[1].value) is int
    assert query_dct.operators[2].value == 50.6
    assert type(query_dct.operators[2].value) is float
    assert query_dct.operators[3].value == True
    assert type(query_dct.operators[3].value) is bool
    assert query_dct.operators[4].value == datetime(2024, 6, 1)
    assert type(query_dct.operators[4].value) is datetime


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


def test_sort_operator():
    class MyNestedClass(BaseModel):
        n: int

    class MyClass(DbModel):
        a: str
        b: int
        c: int
        nested: MyNestedClass

    sort_operator = sort(
        (MyClass.nested.n, -1), (MyClass.b, 1), (MyClass.c, -1), (MyClass.a, 1)
    )
    assert sort_dict(sort_operators=sort_operator) == {
        "nested.n": -1,
        "b": 1,
        "c": -1,
        "a": 1,
    }

    with pytest.raises(
        ValueError, match="Only values 1 ascending and -1 descending are valid"
    ):
        sort_dict(sort_operators=sort((MyClass.a, 2)))


def test_mount_query_string_with_sort():
    class MyClass(DbModel):
        attr_1: str
        attr_2: str
        attr_3: str

    input_dict = {
        "attr_1_eq": "attr 1",
        "attr_2_in": "['value_1', 'value_2']",
        "attr_3_gte": "10",
        "_sort": "[['attr_1', 1], ['attr_2', -1]]",
    }

    query, sort_operator = mount_query_filter(
        Model=MyClass, items=input_dict, initial_comparison_operators=[]
    )

    assert query == and_(
        eq(MyClass.attr_1, "attr 1"),
        in_(MyClass.attr_2, ["value_1", "value_2"]),
        gte(MyClass.attr_3, 10),
    )
    assert sort_operator == sort((MyClass.attr_1, 1), (MyClass.attr_2, -1))


def test_query_with_magic_methods():
    class MyRefClass(DbModel):
        attr_ref: str
        _collection: ClassVar = "my_ref_class"

    class MyMagicClass(DbModel):
        attr_1: int
        attr_2: int
        attr_3: list[MyRefClass | Id]
        _collection: ClassVar = "my_magic_class"

    query_eq_magic_list = MyMagicClass.attr_3 == [
        "628b7e33e36332a5dc17a0f7",
        "628b7e5de36332a5dc17a119",
    ]
    query_eq_list = eq(
        MyMagicClass.attr_3, ["628b7e33e36332a5dc17a0f7", "628b7e5de36332a5dc17a119"]
    )

    query_lt_magic = MyMagicClass.attr_1 < 123
    query_lt = lt(MyMagicClass.attr_1, 123)
    assert query_lt_magic == query_lt

    query_lte_magic = MyMagicClass.attr_1 <= 123
    query_lte = lte(MyMagicClass.attr_1, 123)
    assert query_lte_magic == query_lte

    query_eq_magic = MyMagicClass.attr_1 == 123
    query_eq = eq(MyMagicClass.attr_1, 123)
    assert query_eq_magic == query_eq

    query_ne_magic = MyMagicClass.attr_1 != 123
    query_ne = ne(MyMagicClass.attr_1, 123)
    assert query_ne_magic == query_ne

    query_gt_magic = MyMagicClass.attr_1 > 123
    query_gt = gt(MyMagicClass.attr_1, 123)
    assert query_gt_magic == query_gt

    query_gte_magic = MyMagicClass.attr_1 >= 123
    query_gte = gte(MyMagicClass.attr_1, 123)
    assert query_gte_magic == query_gte

    query_and_magic = ((MyMagicClass.attr_1 >= 100) | (MyMagicClass.attr_1 <= 200)) & (
        MyMagicClass.attr_2 > 10
    )
    query_and = and_(
        or_(gte(MyMagicClass.attr_1, 100), lte(MyMagicClass.attr_1, 200)),
        gt(MyMagicClass.attr_2, 10),
    )
    assert query_and_magic == query_and

    query_or_magic = (MyMagicClass.attr_1 == 100) & (MyMagicClass.attr_2 == 200) | (
        MyMagicClass.attr_1 > 10
    )
    query_or = or_(
        and_(eq(MyMagicClass.attr_1, 100), eq(MyMagicClass.attr_2, 200)),
        gt(MyMagicClass.attr_1, 10),
    )
    assert query_or_magic == query_or
