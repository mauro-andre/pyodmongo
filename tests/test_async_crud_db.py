from pyodmongo import (
    AsyncDbEngine,
    DbModel,
    SaveResponse,
    DeleteResponse,
    ResponsePaginate,
    Id,
    Field,
)
from pyodmongo.queries import eq, gte, gt, mount_query_filter
from pyodmongo.engine.utils import consolidate_dict
from pydantic import ConfigDict
from typing import ClassVar
from bson import ObjectId
from datetime import datetime
import pytest
import pytest_asyncio

mongo_uri = "mongodb://localhost:27017"
db_name = "pyodmongo_pytest"
db = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name)


class MyClass(DbModel):
    attr1: str
    attr2: str
    random_number: int | None = None
    _collection: ClassVar = "my_class_test"


@pytest_asyncio.fixture()
async def drop_collection():
    await db._db[MyClass._collection].drop()
    yield MyClass(attr1="attr_1", attr2="attr_2")
    await db._db[MyClass._collection].drop()


@pytest_asyncio.fixture()
async def create_100_docs_in_db():
    obj_list = []
    for n in range(1, 101):
        obj_list.append(MyClass(attr1="Value 1", attr2="Value 2", random_number=n))
    await db.save_all(obj_list)


@pytest.fixture()
def new_obj():
    yield MyClass(attr1="attr_1", attr2="attr_2")


@pytest.mark.asyncio
async def test_check_if_create_a_new_doc_on_save(drop_collection, new_obj):
    result: SaveResponse = await db.save(new_obj)
    assert ObjectId.is_valid(result.upserted_id)
    assert new_obj.id == result.upserted_id
    assert isinstance(new_obj.created_at, datetime)
    assert isinstance(new_obj.updated_at, datetime)
    assert new_obj.created_at == new_obj.updated_at


@pytest.mark.asyncio
async def test_create_and_delete_one(drop_collection, new_obj):
    result: SaveResponse = await db.save(new_obj)
    assert result.upserted_id is not None
    id = result.upserted_id
    query = eq(MyClass.id, id)
    result: DeleteResponse = await db.delete_one(Model=MyClass, query=query)
    assert result.deleted_count == 1


@pytest.mark.asyncio
async def test_find_one(drop_collection, new_obj):
    result: SaveResponse = await db.save(new_obj)
    id_returned = result.upserted_id
    obj_found = await db.find_one(MyClass, eq(MyClass.id, id_returned))

    assert isinstance(obj_found, MyClass)
    assert obj_found.id == id_returned


@pytest.fixture()
def objs() -> list[SaveResponse]:
    objs = [
        MyClass(attr1="attr_1", attr2="attr_2"),
        MyClass(attr1="attr_1", attr2="attr_2"),
        MyClass(attr1="attr_1", attr2="attr_2"),
        MyClass(attr1="attr_3", attr2="attr_4"),
        MyClass(attr1="attr_3", attr2="attr_4"),
        MyClass(attr1="attr_5", attr2="attr_6"),
    ]
    return objs


@pytest.mark.asyncio
async def test_save_all_created(drop_collection, objs):
    response: list[SaveResponse] = await db.save_all(objs)
    upserted_quantity = 0
    for obj_response in response:
        obj_response: SaveResponse
        upserted_quantity += 1 if ObjectId.is_valid(obj_response.upserted_id) else 0

    assert upserted_quantity == 6


@pytest.mark.asyncio
async def test_update_on_save(drop_collection, objs):
    await db.save_all(objs)
    obj = MyClass(attr1="value_1", attr2="value_2")
    response: SaveResponse = await db.save(obj, eq(MyClass.attr1, "attr_3"))

    assert response.matched_count == 2
    assert response.modified_count == 2
    assert response.upserted_id is None


@pytest.mark.asyncio
async def test_delete(drop_collection, objs):
    await db.save_all(objs)
    response: DeleteResponse = await db.delete(MyClass, eq(MyClass.attr1, "attr_1"))
    assert response.deleted_count == 3


@pytest.mark.asyncio
async def test_find_many_without_paginate(drop_collection, create_100_docs_in_db):
    obj_list_50 = await db.find_many(Model=MyClass, query=gt(MyClass.random_number, 50))
    obj_list_100 = await db.find_many(Model=MyClass, query=gt(MyClass.random_number, 0))
    assert len(obj_list_50) == 50
    assert len(obj_list_100) == 100
    assert all(isinstance(obj, MyClass) for obj in obj_list_100)


@pytest.mark.asyncio
async def test_find_many_with_paginate(drop_collection, create_100_docs_in_db):
    response_paginate: ResponsePaginate = await db.find_many(
        Model=MyClass,
        query=gt(MyClass.random_number, 50),
        paginate=True,
        docs_per_page=10,
    )
    assert isinstance(response_paginate, ResponsePaginate)
    assert response_paginate.docs_quantity == 50
    assert len(response_paginate.docs) == 10


@pytest.mark.asyncio
async def test_with_query_and_raw_query_none(drop_collection, create_100_docs_in_db):
    all_obj = await db.find_many(Model=MyClass)
    assert len(all_obj) == 100


@pytest.mark.asyncio
async def test_field_alias():
    class MyClass(DbModel):
        first_name: str = Field(alias="firstName", default=None)
        second_name: str = Field(alias="secondName", default=None)
        third_name: str = None
        _collection: ClassVar = "alias_test"

    await db._db[MyClass._collection].drop()

    obj = MyClass(
        first_name="First Name", second_name="Second Name", third_name="Third Name"
    )
    expected_dict = {
        "_id": None,
        "created_at": None,
        "firstName": "First Name",
        "secondName": "Second Name",
        "third_name": "Third Name",
        "updated_at": None,
    }
    dict_to_save = consolidate_dict(obj=obj, dct={})
    assert dict_to_save == expected_dict
    await db.save(obj)
    obj_found = await db.find_one(Model=MyClass)
    assert obj == obj_found

    await db._db[MyClass._collection].drop()


@pytest.mark.asyncio
async def test_fields_alias_generator():
    def to_camel(string: str) -> str:
        return "".join(word.capitalize() for word in string.split("_"))

    def to_lower_camel(string: str) -> str:
        words = string.split("_")
        return "".join(words[:1] + [word.capitalize() for word in words[1:]])

    class MyClass(DbModel):
        first_name: str = None
        second_name: str = None
        third_name: str = None
        _collection: ClassVar = "alias_test"
        model_config = ConfigDict(alias_generator=to_lower_camel)

    await db._db[MyClass._collection].drop()

    obj = MyClass(
        first_name="First Name", second_name="Second Name", third_name="Third Name"
    )
    dict_to_save = consolidate_dict(obj=obj, dct={})
    expected_dict = {
        "_id": None,
        "createdAt": None,
        "firstName": "First Name",
        "secondName": "Second Name",
        "thirdName": "Third Name",
        "updatedAt": None,
    }
    assert dict_to_save == expected_dict
    await db.save(obj)
    obj_found = await db.find_one(Model=MyClass)
    assert obj == obj_found
    await db._db[MyClass._collection].drop()


@pytest.mark.asyncio
async def test_find_many_with_zero_results(drop_collection):
    await db.save(obj=drop_collection)
    result = await db.find_many(
        Model=MyClass, query=eq(MyClass.attr1, "value_that_not_exists"), paginate=True
    )

    assert result.page_quantity == 0
    assert result.docs_quantity == 0
    assert result.docs == []


@pytest.mark.asyncio
async def test_find_one_with_zero_results(drop_collection):
    await db.save(obj=drop_collection)
    result = await db.find_one(
        Model=MyClass, query=eq(MyClass.attr1, "value_that_not_exists")
    )

    assert result is None


@pytest.mark.asyncio
async def test_delete_one_type_error_when_query_is_not_comparison_or_logical_operator():
    with pytest.raises(
        TypeError,
        match='query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await db.delete_one(Model=MyClass, query="string")


@pytest.mark.asyncio
async def test_delete_type_error_when_query_is_not_comparison_or_logical_operator():
    with pytest.raises(
        TypeError,
        match='query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await db.delete(Model=MyClass, query="string")


@pytest.mark.asyncio
async def test_save_type_error_when_query_is_not_comparison_or_logical_operator(
    drop_collection,
):
    with pytest.raises(
        TypeError,
        match='query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await db.save(obj=drop_collection, query="string")


@pytest.mark.asyncio
async def test_find_one_type_error_when_query_is_not_comparison_or_logical_operator():
    with pytest.raises(
        TypeError,
        match='query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await db.find_one(Model=MyClass, query="string")


@pytest.mark.asyncio
async def test_find_many_type_error_when_query_is_not_comparison_or_logical_operator():
    with pytest.raises(
        TypeError,
        match='query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await db.find_many(Model=MyClass, query="string")


class MyModelRegex(DbModel):
    attr_1: str
    attr_2: str = "Default value"
    _collection: ClassVar = "my_model_regex"


@pytest_asyncio.fixture
async def create_regex_collection():

    await db._db[MyModelRegex._collection].drop()
    obj_list = [
        MyModelRegex(attr_1="Agroindústria"),
        MyModelRegex(attr_1="Agro-indústria"),
        MyModelRegex(attr_1="indústria agro"),
        MyModelRegex(attr_1="indústriaagro"),
    ]
    await db.save_all(obj_list=obj_list)
    yield
    await db._db[MyModelRegex._collection].drop()


@pytest.mark.asyncio
async def test_find_regex(create_regex_collection):
    input_dict = {"attr_1_in": "['/^ind[uúû]stria/i']"}
    query = mount_query_filter(
        Model=MyModelRegex, items=input_dict, initial_comparison_operators=[]
    )
    results = await db.find_many(Model=MyModelRegex, query=query)
    assert len(results) == 2


class AsDict1(DbModel):
    attr_1: str
    _collection: ClassVar = "as_dict_1"


class AsDict2(DbModel):
    attr_2: str
    as_dict_1: list[AsDict1 | Id]
    _collection: ClassVar = "as_dict_2"


@pytest_asyncio.fixture
async def create_find_dict_collection():
    await db._db[AsDict1._collection].drop()
    await db._db[AsDict2._collection].drop()

    obj1 = AsDict1(attr_1="Obj 1")
    obj2 = AsDict1(attr_1="Obj 2")
    await db.save_all([obj1, obj2])
    obj3 = AsDict2(attr_2="Obj 3", as_dict_1=[obj1, obj2])
    obj4 = AsDict2(attr_2="Obj 4", as_dict_1=[obj2, obj1])
    obj5 = AsDict2(attr_2="Obj 4", as_dict_1=[obj2, obj1])
    obj6 = AsDict2(attr_2="Obj 4", as_dict_1=[obj2, obj1])
    await db.save_all([obj3, obj4, obj5, obj6])

    yield
    await db._db[AsDict1._collection].drop()
    await db._db[AsDict2._collection].drop()


@pytest.mark.asyncio
async def test_find_as_dict(create_find_dict_collection):
    obj_list = await db.find_many(Model=AsDict2, as_dict=True, populate=True)
    assert len(obj_list) == 4
    assert type(obj_list) is list
    for dct in obj_list:
        assert type(dct) == dict
    obj_dict = await db.find_one(Model=AsDict2, as_dict=True, populate=True)
    assert type(obj_dict) == dict
