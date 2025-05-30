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

    print(MyModel4.attr_5.model_2.attr_3)
    # print(vars(MyModel3.attr_5.attr_3))
