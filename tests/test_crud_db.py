from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar
import pytest

mongo_uri = 'mongodb://localhost:27017'
db_name = 'pyodmongo_pytest'
db = DbEngine(mongo_uri=mongo_uri, db_name=db_name)


class MyClass(DbModel):
    attr1: str
    attr2: str
    _collection: ClassVar = 'my_class_test'


# {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
# {'n': 1, 'upserted': ObjectId('64ead6318257a081b9709d59'), 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}

@pytest.fixture()
def drop_collection():
    db._db[MyClass._collection].drop()
    yield
    db._db[MyClass._collection].drop()


def test_check_if_create_a_new_doc_on_save(drop_collection):
    obj = MyClass(attr1='attr_1', attr2='attr_2')
    result = db.save(obj)
    assert result.get('upserted') is not None


def test_create_and_delete_one(drop_collection):
    obj = MyClass(attr1='attr_1', attr2='attr_2')
    result = db.save(obj)
    assert result.get('upserted') is not None
    id = result.get('upserted')
    query = eq(MyClass.id, id)
    result = db.delete_one(Model=MyClass, query=query)
    assert result.get('document_deleted') == 1
