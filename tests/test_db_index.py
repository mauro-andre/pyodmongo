from pyodmongo import DbModel, Field, DbEngine, AsyncDbEngine
from pymongo import IndexModel, ASCENDING, DESCENDING
from typing import ClassVar
import pytest
import pytest_asyncio


mongo_uri = 'mongodb://localhost:27017'
db_name = 'pyodmongo_pytest'
sync_db = DbEngine(mongo_uri=mongo_uri, db_name=db_name)
async_db = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name)


class MyClass(DbModel):
    attr_0: str
    attr_1: str = Field(index=True)
    attr_2: str = Field(unique=True)
    attr_3: str = Field(text_index=True)
    attr_4: str = Field(index=True, text_index=True, default_language='portuguese')
    _collection: ClassVar = 'my_class'


class MyClass2(DbModel):
    attr_5: str
    attr_6: str = Field(index=True)
    _collection: ClassVar = 'my_class_2'


@pytest.fixture()
def sync_drop_collection():
    sync_db._db[MyClass._collection].drop()
    yield
    sync_db._db[MyClass._collection].drop()


@pytest_asyncio.fixture()
async def async_drop_collection():
    await async_db._db[MyClass._collection].drop()
    yield
    await async_db._db[MyClass._collection].drop()


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
    assert hasattr(MyClass, '_init_indexes')
    assert len(MyClass._init_indexes) == 3
    assert all(type(item) is IndexModel for item in MyClass._init_indexes)


def test_sync_check_index_in_db(sync_drop_collection):
    obj = MyClass(attr_0='attr_0', attr_1='attr_1', attr_2='attr_2', attr_3='attr_3', attr_4='attr_4')
    result = sync_db.save(obj)
    indexes_in_db = sync_db._db[MyClass._collection].index_information()
    assert 'attr_0' not in indexes_in_db
    assert 'attr_1' in indexes_in_db
    assert 'attr_2' not in indexes_in_db
    assert 'attr_3' not in indexes_in_db
    assert 'attr_4' in indexes_in_db
    assert 'attr_3' in indexes_in_db['texts']['weights']
    assert 'attr_4' in indexes_in_db['texts']['weights']


@pytest.mark.asyncio
async def test_async_check_index_in_db(async_drop_collection):
    obj = MyClass(attr_0='attr_0', attr_1='attr_1', attr_2='attr_2', attr_3='attr_3', attr_4='attr_4')
    result = await async_db.save(obj)
    indexes_in_db = await async_db._db[MyClass._collection].index_information()
    assert 'attr_0' not in indexes_in_db
    assert 'attr_1' in indexes_in_db
    assert 'attr_2' not in indexes_in_db
    assert 'attr_3' not in indexes_in_db
    assert 'attr_4' in indexes_in_db
    assert 'attr_3' in indexes_in_db['texts']['weights']
    assert 'attr_4' in indexes_in_db['texts']['weights']
    assert indexes_in_db['texts']['default_language'] == 'portuguese'


def test_create_indexes_on_inheritance(sync_drop_collection):
    class InheritanceClass(MyClass):
        attr_5: str = Field(index=True)

    obj = InheritanceClass(attr_0='attr_0',
                           attr_1='attr_1',
                           attr_2='attr_2',
                           attr_3='attr_3',
                           attr_4='attr_4',
                           attr_5='attr_5')

    result = sync_db.save(obj)
    indexes_in_db = sync_db._db[MyClass._collection].index_information()
    assert 'attr_0' not in indexes_in_db
    assert 'attr_1' in indexes_in_db
    assert 'attr_2' not in indexes_in_db
    assert 'attr_3' not in indexes_in_db
    assert 'attr_4' in indexes_in_db
    assert 'attr_5' in indexes_in_db
    assert 'attr_3' in indexes_in_db['texts']['weights']
    assert 'attr_4' in indexes_in_db['texts']['weights']


def test_create_indexes_on_two_inheritance():
    class MyClass3(MyClass, MyClass2):
        attr_7: str = Field(index=True)

    sync_db._db[MyClass._collection].drop()
    obj = MyClass3(attr_0='attr_0',
                   attr_1='attr_1',
                   attr_2='attr_2',
                   attr_3='attr_3',
                   attr_4='attr_4',
                   attr_5='attr_5',
                   attr_6='attr_6',
                   attr_7='attr_7',
                   )
    result = sync_db.save(obj)
    indexes_in_db = sync_db._db[MyClass._collection].index_information()
    assert 'attr_0' not in indexes_in_db
    assert 'attr_1' in indexes_in_db
    assert 'attr_2' not in indexes_in_db
    assert 'attr_3' not in indexes_in_db
    assert 'attr_4' in indexes_in_db
    assert 'attr_5' not in indexes_in_db
    assert 'attr_6' in indexes_in_db
    assert 'attr_7' in indexes_in_db
    assert 'attr_3' in indexes_in_db['texts']['weights']
    assert 'attr_4' in indexes_in_db['texts']['weights']
    sync_db._db[MyClass._collection].drop()


def test_create_custom_indexes():

    class MyClassCustomIndex(DbModel):
        attr_0: str = Field(default=None, index=True)
        attr_1: str = Field(default=None)
        _collection: ClassVar = 'my_class_custom_index'
        _indexes: ClassVar = [
            IndexModel([('attr_0', ASCENDING), ('attr_1', DESCENDING)], name='attr_0_and_attr_1')
        ]

    sync_db._db[MyClassCustomIndex._collection].drop()

    obj = MyClassCustomIndex()
    sync_db.save(obj)
    indexes_in_db = sync_db._db[MyClassCustomIndex._collection].index_information()
    assert 'attr_0_and_attr_1' in indexes_in_db
    assert 'attr_0' not in indexes_in_db
    assert 'attr_1' not in indexes_in_db
    assert len(indexes_in_db['attr_0_and_attr_1']['key']) == 2
    assert indexes_in_db['attr_0_and_attr_1']['key'][0] == ('attr_0', 1)
    assert indexes_in_db['attr_0_and_attr_1']['key'][1] == ('attr_1', -1)

    sync_db._db[MyClassCustomIndex._collection].drop()


@pytest.mark.asyncio
async def test_async_create_custom_indexes():

    class MyClassCustomIndex(DbModel):
        attr_0: str = Field(default=None, index=True)
        attr_1: str = Field(default=None)
        _collection: ClassVar = 'my_class_custom_index'
        _indexes: ClassVar = [
            IndexModel([('attr_0', ASCENDING), ('attr_1', DESCENDING)], name='attr_0_and_attr_1')
        ]

    await async_db._db[MyClassCustomIndex._collection].drop()

    obj = MyClassCustomIndex()
    await async_db.save(obj)
    indexes_in_db = sync_db._db[MyClassCustomIndex._collection].index_information()
    assert 'attr_0_and_attr_1' in indexes_in_db
    assert 'attr_0' not in indexes_in_db
    assert 'attr_1' not in indexes_in_db
    assert len(indexes_in_db['attr_0_and_attr_1']['key']) == 2
    assert indexes_in_db['attr_0_and_attr_1']['key'][0] == ('attr_0', 1)
    assert indexes_in_db['attr_0_and_attr_1']['key'][1] == ('attr_1', -1)

    sync_db._db[MyClassCustomIndex._collection].drop()
