from datetime import timezone, timedelta
from typing import ClassVar
import pytest
import pytest_asyncio
from pyodmongo import (
    AsyncDbEngine,
    DbEngine,
    DbModel,
    Field,
    DbResponse,
    ResponsePaginate,
)
from bson import ObjectId
import copy
from faker import Faker

mongo_uri = "mongodb://localhost:27017"
db_name = "pyodmongo_pytest"
tz_info = timezone(timedelta(hours=-3))

async_engine = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name, tz_info=tz_info)
engine = DbEngine(mongo_uri=mongo_uri, db_name=db_name, tz_info=tz_info)

fake = Faker()


@pytest_asyncio.fixture()
async def drop_db():
    await async_engine._client.drop_database(db_name)
    engine._client.drop_database(db_name)
    yield
    # await async_engine._client.drop_database(db_name)
    # engine._client.drop_database(db_name)


@pytest.mark.asyncio
async def test_save_all(drop_db):
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

    id_0 = copy.copy(obj_0.id)
    id_1 = copy.copy(obj_1.id)
    id_2 = copy.copy(obj_2.id)
    id_3 = copy.copy(obj_3.id)

    obj_0.attr_0 = "zero_zero"
    obj_1.attr_0 = "one_one"
    obj_2.attr_2 = "two_two"
    obj_3.attr_2 = "three_three"

    await async_engine.save_all([obj_1, obj_3])
    engine.save_all([obj_0, obj_2])

    assert obj_0.id == id_0
    assert obj_1.id == id_1
    assert obj_2.id == id_2
    assert obj_3.id == id_3


@pytest.mark.asyncio
async def test_save(drop_db):
    class MyClass0(DbModel):
        attr_0: str = Field(index=True)
        attr_1: int = Field(index=True)
        _collection: ClassVar = "my_class_0"

    class MyClass1(DbModel):
        attr_2: str = Field(index=True)
        attr_3: int = Field(index=True)
        _collection: ClassVar = "my_class_1"

    obj_0 = MyClass0(attr_0="zero", attr_1=0)
    obj_1 = MyClass1(attr_2="two", attr_3=2)

    response_0: DbResponse = await async_engine.save(obj_0)
    response_1: DbResponse = engine.save(obj_1)

    assert obj_0.id == response_0.upserted_ids[0]
    assert obj_1.id == response_1.upserted_ids[0]


@pytest.mark.asyncio
async def test_find(drop_db):
    class MyClass0(DbModel):
        attr_0: str = Field(index=True)
        attr_1: int = Field(index=True)
        _collection: ClassVar = "my_class_0"

    objs_0_49 = [MyClass0(attr_0=fake.name(), attr_1=n) for n in range(0, 50)]
    objs_50_99 = [MyClass0(attr_0=fake.name(), attr_1=n) for n in range(50, 100)]

    await async_engine.save_all(objs_0_49)
    engine.save_all(objs_50_99)

    obj_to_find_0_49: MyClass0 = copy.deepcopy(objs_0_49[24])
    obj_to_find_50_99: MyClass0 = copy.deepcopy(objs_50_99[24])

    obj_found_0_49: MyClass0 = await async_engine.find_one(
        Model=MyClass0, query=MyClass0.id == obj_to_find_0_49.id
    )
    obj_found_50_49: MyClass0 = engine.find_one(
        Model=MyClass0, query=MyClass0.id == obj_to_find_50_99.id
    )

    assert obj_found_0_49 == obj_to_find_0_49
    assert obj_found_50_49 == obj_to_find_50_99

    query_0 = (MyClass0.attr_1 > 10) & (MyClass0.attr_1 <= 20)
    query_1 = (MyClass0.attr_1 > 60) & (MyClass0.attr_1 <= 70)

    result_0: ResponsePaginate = await async_engine.find_many(
        Model=MyClass0, query=query_0, paginate=True, current_page=2, docs_per_page=2
    )
    result_1: ResponsePaginate = engine.find_many(
        Model=MyClass0, query=query_1, paginate=True, current_page=2, docs_per_page=2
    )
    assert result_0.current_page == 2
    assert result_0.page_quantity == 5
    assert result_0.docs_quantity == 10
    assert len(result_0.docs) == 2
    assert result_1.current_page == 2
    assert result_1.page_quantity == 5
    assert result_1.docs_quantity == 10
    assert len(result_1.docs) == 2
