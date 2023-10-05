from pyodmongo import DbModel, Id


def test_empty_dict():
    class MyModel1(DbModel):
        attr1: str
        _collection = "my_model_1"

    class MyModel2(DbModel):
        attr2: str
        my_model_1: MyModel1 | Id
        _collection = "my_model_2"

    class MyModel3(DbModel):
        attr3: str
        my_model_2: MyModel2 | Id
        _collection = "my_model_3"

    dct = {
        "attr3": "attr3",
        "my_model_2": {},
    }
    obj = MyModel3(**dct)
    assert obj.model_dump() == {
        "attr3": "attr3",
        "my_model_2": None,
        "id": None,
        "created_at": None,
        "updated_at": None,
    }
