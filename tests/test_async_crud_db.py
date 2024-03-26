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
    attr_2: str
    attr_3: str
    _collection: ClassVar = "as_dict_1"


class AsDict11(DbModel):
    attr_2: str
    attr_3: str
    _collection: ClassVar = "as_dict_1"


class AsDict2(DbModel):
    attr_4: str
    as_dict_1: list[AsDict1 | Id]
    _collection: ClassVar = "as_dict_2"


class AsDict22(DbModel):
    attr_4: str
    as_dict_1: list[AsDict11 | Id]
    _collection: ClassVar = "as_dict_2"


@pytest_asyncio.fixture
async def create_as_dict_find_dict_collection():
    await db._db[AsDict1._collection].drop()
    await db._db[AsDict2._collection].drop()
    yield
    await db._db[AsDict1._collection].drop()
    await db._db[AsDict2._collection].drop()


@pytest.mark.asyncio
async def test_find_as_dict(create_as_dict_find_dict_collection):
    obj1 = AsDict1(attr_1="Obj 1", attr_2="Obj 1", attr_3="Obj 1")
    obj2 = AsDict1(attr_1="Obj 2", attr_2="Obj 2", attr_3="Obj 2")
    obj3 = AsDict1(attr_1="Obj 3", attr_2="Obj 3", attr_3="Obj 3")
    obj4 = AsDict1(attr_1="Obj 4", attr_2="Obj 4", attr_3="Obj 4")
    obj5 = AsDict1(attr_1="Obj 5", attr_2="Obj 5", attr_3="Obj 5")
    obj6 = AsDict1(attr_1="Obj 6", attr_2="Obj 6", attr_3="Obj 6")
    obj7 = AsDict1(attr_1="Obj 7", attr_2="Obj 7", attr_3="Obj 7")
    obj8 = AsDict1(attr_1="Obj 8", attr_2="Obj 8", attr_3="Obj 8")
    await db.save_all([obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8])
    obj9 = AsDict2(attr_4="Obj 9", as_dict_1=[obj1, obj2])
    obj10 = AsDict2(attr_4="Obj 10", as_dict_1=[obj3, obj4])
    obj11 = AsDict2(attr_4="Obj 11", as_dict_1=[obj5, obj6])
    obj12 = AsDict2(attr_4="Obj 12", as_dict_1=[obj7, obj8])
    await db.save_all([obj9, obj10, obj11, obj12])

    obj_list = await db.find_many(Model=AsDict22, as_dict=True, populate=True)
    assert len(obj_list) == 4
    assert type(obj_list) is list
    for dct in obj_list:
        assert type(dct) == dict
    obj_dict = await db.find_one(Model=AsDict2, as_dict=True, populate=True)
    assert type(obj_dict) == dict


class A(DbModel):
    a1: str = "A"
    _collection: ClassVar = "a"


class B(DbModel):
    b1: A | Id
    _collection: ClassVar = "b"


class C(DbModel):
    b1: A | Id
    b2: list[B | Id]
    _collection: ClassVar = "c"


class D(DbModel):
    d1: list[C | Id]
    _collection: ClassVar = "d"


@pytest_asyncio.fixture
async def create_find_dict_collection():
    await db._db[A._collection].drop()
    await db._db[B._collection].drop()
    await db._db[C._collection].drop()
    await db._db[D._collection].drop()
    yield
    await db._db[A._collection].drop()
    await db._db[B._collection].drop()
    await db._db[C._collection].drop()
    await db._db[D._collection].drop()


@pytest.mark.asyncio
async def test_recursive_reference_pipeline(create_find_dict_collection):

    a1 = A()
    a2 = A()
    a3 = A()
    a4 = A()
    a5 = A()
    a6 = A()
    await db.save_all([a1, a2, a3, a4, a5, a6])
    b1 = B(b1=a3)
    b2 = B(b1=a4)
    b3 = B(b1=a5)
    b4 = B(b1=a6)
    await db.save_all([b1, b2, b3, b4])
    c1 = C(b1=a1, b2=[b1, b2])
    c2 = C(b1=a2, b2=[b3, b4])
    await db.save_all([c1, c2])
    d1 = D(d1=[c1, c2])
    await db.save(d1)

    d: D = await db.find_one(Model=D, populate=True)

    assert d.d1[0].b2[0].b1.a1 == "A"


class ClassA(DbModel):
    attr_1: str = "A String 1"
    attr_2: str = "A String 2"
    _collection: ClassVar = "col_a"


class ClassB(DbModel):
    attr_3: str = "A String 3"
    a: ClassA | Id
    _collection: ClassVar = "col_b"


@pytest_asyncio.fixture()
async def drop_collections():
    await db._db[ClassA._collection].drop()
    await db._db[ClassB._collection].drop()
    yield
    await db._db[ClassA._collection].drop()
    await db._db[ClassB._collection].drop()


@pytest.mark.asyncio
async def test_find_nested_field_query(drop_collections):
    obj_a = ClassA()
    await db.save(obj=obj_a)
    obj_b = ClassB(a=obj_a)
    await db.save(obj=obj_b)
    query = eq(ClassB.a, obj_a.id)
    result = await db.find_many(Model=ClassB, query=query, populate=True)
    assert result == [obj_b]


@pytest.mark.asyncio
async def test_find_nested_field_mount_query(drop_collections):
    obj_a = ClassA()
    await db.save(obj=obj_a)
    obj_b = ClassB(a=obj_a)
    await db.save(obj=obj_b)
    input_dict = {"a": obj_a.id}
    query = mount_query_filter(
        Model=ClassB, items=input_dict, initial_comparison_operators=[]
    )
    result = await db.find_many(Model=ClassB, query=query, populate=True)
    assert result == [obj_b]
