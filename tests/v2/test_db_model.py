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


def test_db_field_eq():
    class MyModel1(DbModel):
        attr_1: str

    class MyModel2(DbModel):
        attr_1: str
        model_1: MyModel1

    assert (MyModel1.attr_1 == "abc") == {"attr_1": {"$eq": "abc"}}
    assert (MyModel2.model_1.attr_1 == "abc") == {"model_1.attr_1": {"$eq": "abc"}}
    assert not MyModel2.attr_1 == MyModel1.attr_1
