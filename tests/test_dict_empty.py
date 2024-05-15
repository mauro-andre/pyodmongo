from pyodmongo import DbModel, Id


def test_empty_dict():
    class MyModel1(DbModel):
        attr1: str | None
        _collection = "my_model_1"

    class MyModel2(DbModel):
        attr2: str | None
        attr2_list: list | None = []
        my_model_1: MyModel1 | Id | None
        _collection = "my_model_2"

    class MyModel3(DbModel):
        attr3: str | None
        my_model_2: MyModel2 | Id | None
        my_model_2_2: MyModel2 | Id | None
        my_model_2_3: MyModel2 | Id | None
        my_model_2_4: MyModel2 | Id | None
        _collection = "my_model_3"

    dct = {
        "attr3": "attr3",
        "my_model_2": {
            "attr2": "Escrito",
            "attr2_list": [],
            "my_model_1": {"attr1": {}},
        },
        "my_model_2_2": {"my_model_1": {}, "attr2_list": None},
        "my_model_2_3": {},
        "my_model_2_4": {"attr2": None, "attr2_list": [], "my_model_1": {}},
    }
    obj = MyModel3(**dct)
    assert obj.model_dump() == {
        "attr3": "attr3",
        "my_model_2": {
            "id": None,
            "created_at": None,
            "updated_at": None,
            "attr2": "Escrito",
            "attr2_list": [],
            "my_model_1": None,
        },
        "my_model_2_2": None,
        "my_model_2_3": None,
        "my_model_2_4": {
            "id": None,
            "created_at": None,
            "updated_at": None,
            "attr2": None,
            "attr2_list": [],
            "my_model_1": None,
        },
        "id": None,
        "created_at": None,
        "updated_at": None,
    }
