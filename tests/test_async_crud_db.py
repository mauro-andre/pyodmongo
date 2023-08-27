from pyodmongo import AsyncDbEngine, DbModel
from typing import ClassVar
import pytest

mongo_uri = 'mongodb://localhost:27017'
db_name = 'pyodmongo_pytest'
db = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name)


class MyClass(DbModel):
    attr1: str
    attr2: str
    _collection: ClassVar = 'my_class_test'


# {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
# {'n': 1, 'upserted': ObjectId('64ead6318257a081b9709d59'), 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}

@pytest.mark.asyncio
async def test_check_if_create_a_new_doc_on_save():
    obj = MyClass(attr1='attr_1', attr2='attr_2')
    db._db[MyClass._collection].drop()
    result = await db.save(obj)
    assert result.get('upserted') is not None
    db._db[MyClass._collection].drop()
