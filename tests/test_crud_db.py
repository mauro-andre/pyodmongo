from pyodmongo import DbEngine, DbModel, SaveResponse, DeleteResponse
from pyodmongo.queries import eq
from typing import ClassVar
from bson import ObjectId
import pytest

mongo_uri = 'mongodb://localhost:27017'
db_name = 'pyodmongo_pytest'
db = DbEngine(mongo_uri=mongo_uri, db_name=db_name)


class MyClass(DbModel):
    attr1: str
    attr2: str
    _collection: ClassVar = 'my_class_test'


@pytest.fixture()
def drop_collection():
    db._db[MyClass._collection].drop()
    yield MyClass(attr1='attr_1', attr2='attr_2')
    db._db[MyClass._collection].drop()


@pytest.fixture()
def new_obj() -> type[MyClass]:
    yield MyClass(attr1='attr_1', attr2='attr_2')


def test_check_if_create_a_new_doc_on_save(drop_collection, new_obj):
    result: SaveResponse = db.save(new_obj)
    assert ObjectId.is_valid(result.upserted_id)


def test_create_and_delete_one(drop_collection, new_obj):
    result: SaveResponse = db.save(new_obj)
    assert result.upserted_id is not None
    id = result.upserted_id
    query = eq(MyClass.id, id)
    result: DeleteResponse = db.delete_one(Model=MyClass, query=query)
    assert result.deleted_count == 1


def test_find_one(drop_collection, new_obj):
    result: SaveResponse = db.save(new_obj)
    id_returned = result.upserted_id
    obj_found = db.find_one(MyClass, eq(MyClass.id, id_returned))

    assert isinstance(obj_found, MyClass)
    assert obj_found.id == id_returned


@pytest.fixture()
def objs() -> list[SaveResponse]:
    objs = [
        MyClass(attr1='attr_1', attr2='attr_2'),
        MyClass(attr1='attr_1', attr2='attr_2'),
        MyClass(attr1='attr_1', attr2='attr_2'),
        MyClass(attr1='attr_3', attr2='attr_4'),
        MyClass(attr1='attr_3', attr2='attr_4'),
        MyClass(attr1='attr_5', attr2='attr_6'),
    ]
    return objs


def test_save_all_created(drop_collection, objs):
    response: list[SaveResponse] = db.save_all(objs)
    upseted_quantity = 0
    for obj_response in response:
        obj_response: SaveResponse
        upseted_quantity += 1 if ObjectId.is_valid(obj_response.upserted_id) else 0

    assert upseted_quantity == 6


def test_update_on_save(drop_collection, objs):
    db.save_all(objs)
    obj = MyClass(attr1='value_1', attr2='value_2')
    response: SaveResponse = db.save(obj, eq(MyClass.attr1, 'attr_3'))

    assert response.matched_count == 2
    assert response.modified_count == 2
    assert response.upserted_id is None


def test_delete(drop_collection, objs):
    db.save_all(objs)
    response: DeleteResponse = db.delete(MyClass, eq(MyClass.attr1, 'attr_1'))
    assert response.deleted_count == 3
