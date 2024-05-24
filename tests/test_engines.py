from datetime import timezone, timedelta
from typing import ClassVar
import pytest
import pytest_asyncio
from pyodmongo import AsyncDbEngine, DbEngine, DbModel, Field
from bson import ObjectId

mongo_uri = "mongodb://localhost:27017"
db_name = "pyodmongo_pytest"
tz_info = timezone(timedelta(hours=-3))

async_engine = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name, tz_info=tz_info)
engine = DbEngine(mongo_uri=mongo_uri, db_name=db_name, tz_info=tz_info)


@pytest_asyncio.fixture()
async def drop_collection():
    await async_engine._client.drop_database(db_name)
    engine._client.drop_database(db_name)
    yield
    # await async_engine._client.drop_database(db_name)
    # engine._client.drop_database(db_name)


@pytest.mark.asyncio
async def test_save_all_upsert(drop_collection):
    print()

    class MyClass0(DbModel):
        attr_0: str = Field(index=True)
        attr_1: int = Field(index=True)
        _collection: ClassVar = "my_class_0"

    class MyClass1(DbModel):
        attr_2: str = Field(index=True)
        attr_3: int = Field(index=True)
        _collection: ClassVar = "my_class_1"

    obj_0 = MyClass0(attr_0="zero", attr_1=0)
    obj_1 = MyClass0(attr_0="one", attr_1=1)
    obj_2 = MyClass1(attr_2="two", attr_3=2)
    obj_3 = MyClass1(attr_2="three", attr_3=3)

    await async_engine.save_all([obj_0, obj_2])
    engine.save_all([obj_1, obj_3])

    assert ObjectId.is_valid(obj_0.id)
    assert ObjectId.is_valid(obj_1.id)
    assert ObjectId.is_valid(obj_2.id)
    assert ObjectId.is_valid(obj_3.id)
