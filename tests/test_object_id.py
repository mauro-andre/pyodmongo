import pytest
from pyodmongo import DbModel
from bson import ObjectId
from typing import ClassVar


def test_object_id_to_string():
    class MyClass(DbModel):
        _collection: ClassVar = "myclass"

    id_str = "64e66f06ca15379cd00e6453"
    obj_dict_1 = {"id": id_str}
    obj_dict_2 = {"_id": id_str}
    obj_dict_3 = {"id": ObjectId(id_str)}
    obj_dict_4 = {"_id": ObjectId(id_str)}

    obj_1 = MyClass(**obj_dict_1)
    obj_2 = MyClass(**obj_dict_2)
    obj_3 = MyClass(**obj_dict_3)
    obj_4 = MyClass(**obj_dict_4)

    assert obj_1.id == id_str
    assert type(obj_1.id) == str
    assert obj_2.id == id_str
    assert type(obj_2.id) == str
    assert obj_3.id == id_str
    assert type(obj_3.id) == str
    assert obj_4.id == id_str
    assert type(obj_4.id) == str


def test_insert_an_invalid_object_id():
    class MyClass(DbModel):
        _collection: ClassVar = "myclass"

    id_str = "123abc"
    obj_dict = {"id": id_str}
    with pytest.raises(ValueError):
        MyClass(**obj_dict)
