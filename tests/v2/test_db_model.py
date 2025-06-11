from pyodmongo.v2 import DbModel, Id, Field
from typing import Union


def test_db_model():
    class MyModel1(DbModel):
        attr_1: str
        attr_2: int

    class MyModel2(MyModel1):
        attr_3: bool

    class MyModel3(DbModel):
        attr_3_3: str
        model_2: MyModel2

    class MyModel4(DbModel):
        attr_4: str = Field(alias="attr_4_alias")
        attr_5: MyModel3
        attr_6: str | int
        attr_7: Union[str, int]
        attr_8: list[MyModel3]
        attr_9: list[MyModel3 | MyModel2]
        attr_10: list[Union[MyModel3, MyModel2]]

    # print(MyModel4.attr_5.model_2)


def test_db_field_comparisons():
    class MyModel1(DbModel):
        attr_1: str

    class MyModel2(DbModel):
        attr_1: int
        model_1: MyModel1

    # == operador
    assert (MyModel1.attr_1 == "abc") == {"$eq": ["attr_1", "abc"]}
    assert (MyModel2.model_1.attr_1 == "xyz") == {"$eq": ["model_1.attr_1", "xyz"]}
    assert not (MyModel2.attr_1 == MyModel1.attr_1)

    # != operador
    assert (MyModel1.attr_1 != "abc") == {"$ne": ["attr_1", "abc"]}
    assert (MyModel2.model_1.attr_1 != 42) == {"$ne": ["model_1.attr_1", 42]}

    # < operador
    assert (MyModel1.attr_1 < "zzz") == {"$lt": ["attr_1", "zzz"]}
    assert (MyModel2.model_1.attr_1 < 10) == {"$lt": ["model_1.attr_1", 10]}

    # <= operador
    assert (MyModel1.attr_1 <= "zzz") == {"$lte": ["attr_1", "zzz"]}
    assert (MyModel2.model_1.attr_1 <= 5) == {"$lte": ["model_1.attr_1", 5]}

    # > operador
    assert (MyModel1.attr_1 > "aaa") == {"$gt": ["attr_1", "aaa"]}
    assert (MyModel2.model_1.attr_1 > 0) == {"$gt": ["model_1.attr_1", 0]}

    # >= operador
    assert (MyModel1.attr_1 >= "aaa") == {"$gte": ["attr_1", "aaa"]}
    assert (MyModel2.model_1.attr_1 >= 100) == {"$gte": ["model_1.attr_1", 100]}
