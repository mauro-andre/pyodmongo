from pyodmongo import DbModel, Field, DbEngine, AsyncDbEngine
from pymongo import IndexModel
from typing import ClassVar
import pytest
import pytest_asyncio
from bson import SON


mongo_uri = 'mongodb://localhost:27017'
db_name = 'pyodmongo_pytest'
sync_db = DbEngine(mongo_uri=mongo_uri, db_name=db_name)
async_db = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name)


class MyClass(DbModel):
    attr_0: str
    attr_1: str = Field(index=True)
    attr_2: str = Field(unique=True)
    attr_3: str = Field(text_index=True)
    attr_4: str = Field(index=True, text_index=True)
    _collection: ClassVar = 'myclass'


# @pytest.fixture()
# def sync_drop_collection():
#     sync_db._db[MyClass._collection].drop()
#     yield
#     sync_db._db[MyClass._collection].drop()


# @pytest_asyncio.fixture()
# async def async_drop_collection():
#     await async_db._db[MyClass._collection].drop()
#     yield
#     await async_db._db[MyClass._collection].drop()


def test_index_unique_text_index():
    assert not MyClass.model_fields['attr_0']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_0']._attributes_set.get('unique') or False
    assert not MyClass.model_fields['attr_0']._attributes_set.get('text_index') or False

    assert MyClass.model_fields['attr_1']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_1']._attributes_set.get('unique') or False
    assert not MyClass.model_fields['attr_1']._attributes_set.get('text_index') or False

    assert not MyClass.model_fields['attr_2']._attributes_set.get('index') or False
    assert MyClass.model_fields['attr_2']._attributes_set.get('unique') or False
    assert not MyClass.model_fields['attr_2']._attributes_set.get('text_index') or False

    assert not MyClass.model_fields['attr_3']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_3']._attributes_set.get('unique') or False
    assert MyClass.model_fields['attr_3']._attributes_set.get('text_index') or False

    assert MyClass.model_fields['attr_4']._attributes_set.get('index') or False
    assert not MyClass.model_fields['attr_4']._attributes_set.get('unique') or False
    assert MyClass.model_fields['attr_4']._attributes_set.get('text_index') or False


def test_check_index_field():
    assert hasattr(MyClass, '_indexes')
    assert len(MyClass._indexes) == 3
    assert all(type(item) is IndexModel for item in MyClass._indexes)


# def test_check_index_ind_db(sync_drop_collection):
#     obj = MyClass(attr_0='attr_0', attr_1='attr_1', attr_2='attr_2', attr_3='attr_3', attr_4='attr_4')
#     result = sync_db.save(obj)
#     indexes_in_db = sync_db._db[MyClass._collection].list_indexes()
#     for index in indexes_in_db:
#         index: SON
#         print(index['attr1'])
