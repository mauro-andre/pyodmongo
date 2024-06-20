from pyodmongo import (
    AsyncDbEngine,
    MainBaseModel,
    DbModel,
    MainBaseModel,
    DbResponse,
    ResponsePaginate,
    Id,
    Field,
)
from pyodmongo.queries import eq, gte, gt, mount_query_filter, sort, elem_match
from pyodmongo.engines.utils import consolidate_dict
from pydantic import ConfigDict
from typing import ClassVar
from bson import ObjectId
from datetime import datetime, UTC, timezone, timedelta
import pytz
import pytest
import pytest_asyncio


class MyClass(DbModel):
    attr1: str
    attr2: str
    random_number: int | None = None
    _collection: ClassVar = "my_class_test"


@pytest_asyncio.fixture()
async def drop_collection(async_engine):
    await async_engine._db[MyClass._collection].drop()
    yield MyClass(attr1="attr_1", attr2="attr_2")
    await async_engine._db[MyClass._collection].drop()


@pytest_asyncio.fixture()
async def create_100_docs_in_db(async_engine):
    obj_list = []
    for n in range(1, 101):
        obj_list.append(MyClass(attr1="Value 1", attr2="Value 2", random_number=n))
    await async_engine.save_all(obj_list)


@pytest.fixture()
def new_obj():
    yield MyClass(attr1="attr_1", attr2="attr_2")


@pytest.mark.asyncio
async def test_check_if_create_a_new_doc_on_save(
    drop_collection, new_obj, async_engine
):
    result: DbResponse = await async_engine.save(new_obj)
    assert ObjectId.is_valid(result.upserted_ids[0])
    assert new_obj.id == result.upserted_ids[0]
    assert isinstance(new_obj.created_at, datetime)
    assert isinstance(new_obj.updated_at, datetime)
    assert new_obj.created_at == new_obj.updated_at


@pytest.mark.asyncio
async def test_create_and_delete_one(drop_collection, new_obj, async_engine):
    result: DbResponse = await async_engine.save(new_obj)
    assert result.upserted_ids is not None
    id = result.upserted_ids[0]
    query = MyClass.id == id
    result: DbResponse = await async_engine.delete(
        Model=MyClass, query=query, delete_one=True
    )
    assert result.deleted_count == 1


@pytest.mark.asyncio
async def test_find_one(drop_collection, new_obj, async_engine):
    result: DbResponse = await async_engine.save(new_obj)
    id_returned = result.upserted_ids[0]
    obj_found = await async_engine.find_one(MyClass, eq(MyClass.id, id_returned))

    assert isinstance(obj_found, MyClass)
    assert obj_found.id == id_returned


@pytest.fixture()
def objs():
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
async def test_save_all_created(drop_collection, objs, async_engine):
    await async_engine.save_all(objs)
    assert all([ObjectId.is_valid(obj.id) for obj in objs])


@pytest.mark.asyncio
async def test_update_on_save(drop_collection, objs, async_engine):
    await async_engine.save_all(objs)
    obj = MyClass(attr1="value_1", attr2="value_2")
    response: DbResponse = await async_engine.save(obj, eq(MyClass.attr1, "attr_3"))

    assert response.matched_count == 2
    assert response.modified_count == 2
    assert response.upserted_ids == {}


@pytest.mark.asyncio
async def test_delete(drop_collection, objs, async_engine):
    await async_engine.save_all(objs)
    response: DbResponse = await async_engine.delete(
        MyClass, eq(MyClass.attr1, "attr_1")
    )
    assert response.deleted_count == 3


@pytest.mark.asyncio
async def test_find_many_without_paginate(
    drop_collection, create_100_docs_in_db, async_engine
):
    obj_list_50 = await async_engine.find_many(
        Model=MyClass, query=MyClass.random_number > 50
    )
    obj_list_100 = await async_engine.find_many(
        Model=MyClass, query=MyClass.random_number > 0
    )
    assert len(obj_list_50) == 50
    assert len(obj_list_100) == 100
    assert all(isinstance(obj, MyClass) for obj in obj_list_100)


@pytest.mark.asyncio
async def test_find_many_with_paginate(
    drop_collection, create_100_docs_in_db, async_engine
):
    response_paginate: ResponsePaginate = await async_engine.find_many(
        Model=MyClass,
        query=gt(MyClass.random_number, 50),
        paginate=True,
        docs_per_page=10,
    )
    assert isinstance(response_paginate, ResponsePaginate)
    assert response_paginate.docs_quantity == 50
    assert len(response_paginate.docs) == 10


@pytest.mark.asyncio
async def test_with_query_and_raw_query_none(
    drop_collection, create_100_docs_in_db, async_engine
):
    all_obj = await async_engine.find_many(Model=MyClass)
    assert len(all_obj) == 100


@pytest.mark.asyncio
async def test_field_alias(async_engine):
    class MyClass(DbModel):
        first_name: str = Field(alias="firstName", default=None)
        second_name: str = Field(alias="secondName", default=None)
        third_name: str = None
        _collection: ClassVar = "alias_test"

    await async_engine._db[MyClass._collection].drop()

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
    await async_engine.save(obj)
    obj_found = await async_engine.find_one(Model=MyClass)
    assert obj == obj_found
    await async_engine._db[MyClass._collection].drop()


@pytest.mark.asyncio
async def test_fields_alias_generator(async_engine):
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

    await async_engine._db[MyClass._collection].drop()

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
    await async_engine.save(obj)
    obj_found = await async_engine.find_one(Model=MyClass)
    assert obj == obj_found
    await async_engine._db[MyClass._collection].drop()


@pytest.mark.asyncio
async def test_find_many_with_zero_results(drop_collection, async_engine):
    await async_engine.save(obj=drop_collection)
    result = await async_engine.find_many(
        Model=MyClass, query=MyClass.attr1 == "value_that_not_exists", paginate=True
    )

    assert result.page_quantity == 0
    assert result.docs_quantity == 0
    assert result.docs == []


@pytest.mark.asyncio
async def test_find_one_with_zero_results(drop_collection, async_engine):
    await async_engine.save(obj=drop_collection)
    result = await async_engine.find_one(
        Model=MyClass, query=eq(MyClass.attr1, "value_that_not_exists")
    )

    assert result is None


@pytest.mark.asyncio
async def test_delete_one_type_error_when_query_is_not_comparison_or_logical_operator(
    async_engine,
):
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await async_engine.delete(Model=MyClass, query="string", delete_one=True)


@pytest.mark.asyncio
async def test_delete_type_error_when_query_is_not_comparison_or_logical_operator(
    async_engine,
):
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await async_engine.delete(Model=MyClass, query="string")


@pytest.mark.asyncio
async def test_save_type_error_when_query_is_not_comparison_or_logical_operator(
    drop_collection, async_engine
):
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await async_engine.save(obj=drop_collection, query="string")


@pytest.mark.asyncio
async def test_find_one_type_error_when_query_is_not_comparison_or_logical_operator(
    async_engine,
):
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await async_engine.find_one(Model=MyClass, query="string")


@pytest.mark.asyncio
async def test_find_many_type_error_when_query_is_not_comparison_or_logical_operator(
    async_engine,
):
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        await async_engine.find_many(Model=MyClass, query="string")


class MyModelRegex(DbModel):
    attr_1: str
    attr_2: str = "Default value"
    _collection: ClassVar = "my_model_regex"


@pytest_asyncio.fixture
async def create_regex_collection(async_engine: AsyncDbEngine):
    await async_engine._db[MyModelRegex._collection].drop()
    obj_list = [
        MyModelRegex(attr_1="Agroindústria"),
        MyModelRegex(attr_1="Agro-indústria"),
        MyModelRegex(attr_1="indústria agro"),
        MyModelRegex(attr_1="indústriaagro"),
    ]
    await async_engine.save_all(obj_list=obj_list)
    yield
    await async_engine._db[MyModelRegex._collection].drop()


@pytest.mark.asyncio
async def test_find_regex(create_regex_collection, async_engine: AsyncDbEngine):
    input_dict = {"attr_1_in": "['/^ind[uúû]stria/i']"}
    query, _ = mount_query_filter(
        Model=MyModelRegex, items=input_dict, initial_comparison_operators=[]
    )
    results = await async_engine.find_many(Model=MyModelRegex, query=query)
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
async def create_as_dict_find_dict_collection(async_engine: AsyncDbEngine):
    await async_engine._db[AsDict1._collection].drop()
    await async_engine._db[AsDict2._collection].drop()
    yield
    await async_engine._db[AsDict1._collection].drop()
    await async_engine._db[AsDict2._collection].drop()


@pytest.mark.asyncio
async def test_find_as_dict(
    create_as_dict_find_dict_collection, async_engine: AsyncDbEngine
):
    obj1 = AsDict1(attr_1="Obj 1", attr_2="Obj 1", attr_3="Obj 1")
    obj2 = AsDict1(attr_1="Obj 2", attr_2="Obj 2", attr_3="Obj 2")
    obj3 = AsDict1(attr_1="Obj 3", attr_2="Obj 3", attr_3="Obj 3")
    obj4 = AsDict1(attr_1="Obj 4", attr_2="Obj 4", attr_3="Obj 4")
    obj5 = AsDict1(attr_1="Obj 5", attr_2="Obj 5", attr_3="Obj 5")
    obj6 = AsDict1(attr_1="Obj 6", attr_2="Obj 6", attr_3="Obj 6")
    obj7 = AsDict1(attr_1="Obj 7", attr_2="Obj 7", attr_3="Obj 7")
    obj8 = AsDict1(attr_1="Obj 8", attr_2="Obj 8", attr_3="Obj 8")
    await async_engine.save_all([obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8])
    obj9 = AsDict2(attr_4="Obj 9", as_dict_1=[obj1, obj2])
    obj10 = AsDict2(attr_4="Obj 10", as_dict_1=[obj3, obj4])
    obj11 = AsDict2(attr_4="Obj 11", as_dict_1=[obj5, obj6])
    obj12 = AsDict2(attr_4="Obj 12", as_dict_1=[obj7, obj8])
    await async_engine.save_all([obj9, obj10, obj11, obj12])

    obj_list = await async_engine.find_many(Model=AsDict22, as_dict=True, populate=True)
    assert len(obj_list) == 4
    assert type(obj_list) is list
    for dct in obj_list:
        assert type(dct) == dict
    obj_dict = await async_engine.find_one(Model=AsDict2, as_dict=True, populate=True)
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
async def create_find_dict_collection(async_engine: AsyncDbEngine):
    await async_engine._db[A._collection].drop()
    await async_engine._db[B._collection].drop()
    await async_engine._db[C._collection].drop()
    await async_engine._db[D._collection].drop()
    yield
    await async_engine._db[A._collection].drop()
    await async_engine._db[B._collection].drop()
    await async_engine._db[C._collection].drop()
    await async_engine._db[D._collection].drop()


@pytest.mark.asyncio
async def test_recursive_reference_pipeline(
    create_find_dict_collection, async_engine: AsyncDbEngine
):
    a1 = A()
    a2 = A()
    a3 = A()
    a4 = A()
    a5 = A()
    a6 = A()
    await async_engine.save_all([a1, a2, a3, a4, a5, a6])
    b1 = B(b1=a3)
    b2 = B(b1=a4)
    b3 = B(b1=a5)
    b4 = B(b1=a6)
    await async_engine.save_all([b1, b2, b3, b4])
    c1 = C(b1=a1, b2=[b1, b2])
    c2 = C(b1=a2, b2=[b3, b4])
    await async_engine.save_all([c1, c2])
    d1 = D(d1=[c1, c2])
    await async_engine.save(d1)

    d: D = await async_engine.find_one(Model=D, populate=True)

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
async def drop_collections_a_b(async_engine: AsyncDbEngine):
    await async_engine._db[ClassA._collection].drop()
    await async_engine._db[ClassB._collection].drop()
    yield
    await async_engine._db[ClassA._collection].drop()
    await async_engine._db[ClassB._collection].drop()


@pytest.mark.asyncio
async def test_find_nested_field_query(
    drop_collections_a_b, async_engine: AsyncDbEngine
):
    obj_a = ClassA()
    await async_engine.save(obj=obj_a)
    obj_b = ClassB(a=obj_a)
    await async_engine.save(obj=obj_b)
    query = eq(ClassB.a, obj_a.id)
    result = await async_engine.find_many(Model=ClassB, query=query, populate=True)
    assert result == [obj_b]


@pytest.mark.asyncio
async def test_find_nested_field_mount_query(
    drop_collections_a_b, async_engine: AsyncDbEngine
):
    obj_a = ClassA()
    await async_engine.save(obj=obj_a)
    obj_b = ClassB(a=obj_a)
    await async_engine.save(obj=obj_b)
    input_dict = {"a": obj_a.id}
    query, _ = mount_query_filter(
        Model=ClassB, items=input_dict, initial_comparison_operators=[]
    )
    result = await async_engine.find_many(Model=ClassB, query=query, populate=True)
    assert result == [obj_b]


class ClassOne(DbModel):
    attr_1: str = "attr 1"
    _collection: ClassVar = "class_one"


class ClassTwoA(MainBaseModel):
    attr_2_a: str = "attr 2 A"
    class_one: list[ClassOne | Id] | None


class ClassTwoB(MainBaseModel):
    attr_2_b: str = "attr 2 B"
    class_two_a: ClassTwoA | None
    class_two_a_list: list[ClassTwoA] | None


class ClassThree(DbModel):
    attr_3: str = "attr 3"
    class_two_b: ClassTwoB | None
    class_two_b_list: list[ClassTwoB] | None
    _collection: ClassVar = "class_three"


@pytest_asyncio.fixture()
async def drop_collections_one_three(async_engine: AsyncDbEngine):
    await async_engine._db[ClassOne._collection].drop()
    await async_engine._db[ClassThree._collection].drop()
    yield
    await async_engine._db[ClassOne._collection].drop()
    await async_engine._db[ClassThree._collection].drop()


@pytest.mark.asyncio
async def test_nested_list_objects(
    drop_collections_one_three, async_engine: AsyncDbEngine
):
    obj_1 = ClassOne(attr_1="obj_1")
    obj_2 = ClassOne(attr_1="obj_2")
    obj_3 = ClassOne(attr_1="obj_3")
    obj_4 = ClassOne(attr_1="obj_4")
    obj_5 = ClassOne(attr_1="obj_5")
    obj_6 = ClassOne(attr_1="obj_6")
    obj_7 = ClassOne(attr_1="obj_7")
    obj_8 = ClassOne(attr_1="obj_8")
    await async_engine.save_all(
        [obj_1, obj_2, obj_3, obj_4, obj_5, obj_6, obj_7, obj_8]
    )
    obj_9 = ClassTwoA(attr_2_a="obj_9", class_one=[obj_1, obj_2])
    obj_10 = ClassTwoA(attr_2_a="obj_10", class_one=[obj_3, obj_4])
    obj_11 = ClassTwoA(attr_2_a="obj_11", class_one=[obj_5, obj_6])
    obj_12 = ClassTwoA(attr_2_a="obj_12", class_one=[obj_7, obj_8])
    obj_13 = ClassTwoB(
        attr_2_b="obj_13", class_two_a=obj_9, class_two_a_list=[obj_9, obj_10]
    )
    obj_14 = ClassTwoB(
        attr_2_b="obj_14", class_two_a=obj_11, class_two_a_list=[obj_11, obj_12]
    )
    obj_15 = ClassThree(
        attr_3="obj_15", class_two_b=obj_13, class_two_b_list=[obj_13, obj_14]
    )
    await async_engine.save(obj_15)

    obj_found = await async_engine.find_one(Model=ClassThree, populate=True)
    assert obj_found.id == obj_15.id
    assert obj_found.class_two_b.attr_2_b == "obj_13"


class MySortClass(DbModel):
    attr_1: str
    attr_2: int
    attr_3: datetime
    _collection: ClassVar = "my_class_to_sort"


@pytest_asyncio.fixture()
async def drop_collection_for_test_sort(async_engine: AsyncDbEngine):
    await async_engine._db[MySortClass._collection].drop()
    yield
    await async_engine._db[MySortClass._collection].drop()


@pytest.mark.asyncio
async def test_sort_query(drop_collection_for_test_sort, async_engine: AsyncDbEngine):
    obj_list = [
        MySortClass(
            attr_1="Juliet",
            attr_2=100,
            attr_3=datetime(year=2023, month=1, day=20, tzinfo=UTC),
        ),
        MySortClass(
            attr_1="Albert",
            attr_2=50,
            attr_3=datetime(year=2025, month=1, day=20, tzinfo=UTC),
        ),
        MySortClass(
            attr_1="Zack",
            attr_2=30,
            attr_3=datetime(year=2020, month=1, day=20, tzinfo=UTC),
        ),
        MySortClass(
            attr_1="Charlie",
            attr_2=150,
            attr_3=datetime(year=2027, month=1, day=20, tzinfo=UTC),
        ),
        MySortClass(
            attr_1="Albert",
            attr_2=40,
            attr_3=datetime(year=2025, month=1, day=20, tzinfo=UTC),
        ),
    ]
    await async_engine.save_all(obj_list=obj_list)
    sort_oprator = sort((MySortClass.attr_1, 1), (MySortClass.attr_2, 1))
    result_many = await async_engine.find_many(Model=MySortClass, sort=sort_oprator)
    assert result_many[0] == obj_list[4]
    assert result_many[1] == obj_list[1]

    sort_oprator = sort((MySortClass.attr_3, 1))
    result_one = await async_engine.find_one(Model=MySortClass, sort=sort_oprator)
    assert result_one == obj_list[2]

    sort_oprator = ["attr_3", 1]
    with pytest.raises(
        TypeError,
        match='sort argument must be a SortOperator from pyodmongo.queries. If you really need to make a very specific sort, use "raw_sort" argument',
    ):
        result_one = await async_engine.find_one(Model=MySortClass, sort=sort_oprator)

    with pytest.raises(
        TypeError,
        match='sort argument must be a SortOperator from pyodmongo.queries. If you really need to make a very specific sort, use "raw_sort" argument',
    ):
        result_many = await async_engine.find_many(Model=MySortClass, sort=sort_oprator)


class ClassWithDate(DbModel):
    name: str
    date: datetime
    _collection: ClassVar = "class_with_date"


@pytest_asyncio.fixture()
async def drop_collection_class_with_date(async_engine: AsyncDbEngine):
    await async_engine._db[ClassWithDate._collection].drop()
    yield
    await async_engine._db[ClassWithDate._collection].drop()


@pytest.mark.asyncio
async def test_save_and_retrieve_objs_with_datetime(
    drop_collection_class_with_date, async_engine: AsyncDbEngine
):
    tz = timezone(timedelta(hours=-3))
    date = datetime(
        year=2024,
        month=4,
        day=24,
        hour=23,
        minute=0,
        second=0,
        tzinfo=tz,
    )
    obj = ClassWithDate(name="A name", date=date)
    await async_engine.save(obj)
    query = (ClassWithDate.date >= datetime(2024, 4, 24, 22, 30, 0, tzinfo=tz)) & (
        ClassWithDate.date <= datetime(2024, 4, 24, 23, 30, 0, tzinfo=tz)
    )
    obj_found: ClassWithDate = await async_engine.find_one(
        Model=ClassWithDate, query=query
    )
    assert obj_found.date == date


class ModelEmbedded(MainBaseModel):
    attr_1: str
    attr_2: str


class ModelMain(DbModel):
    attr_3: list[ModelEmbedded]
    _collection: ClassVar = "model_elem_match"


@pytest_asyncio.fixture()
async def drop_collection_for_elem_match(async_engine: AsyncDbEngine):
    await async_engine._db[ModelMain._collection].drop()
    yield
    await async_engine._db[ModelMain._collection].drop()


@pytest.mark.asyncio
async def test_elem_match_in_db(
    drop_collection_for_elem_match, async_engine: AsyncDbEngine
):
    obj_embedded_0 = ModelEmbedded(attr_1="one", attr_2="one")
    obj_embedded_1 = ModelEmbedded(attr_1="two", attr_2="two")
    obj_embedded_2 = ModelEmbedded(attr_1="one", attr_2="two")
    obj_embedded_3 = ModelEmbedded(attr_1="two", attr_2="one")

    obj_db_0 = ModelMain(attr_3=[obj_embedded_0, obj_embedded_1])
    obj_db_1 = ModelMain(attr_3=[obj_embedded_2, obj_embedded_3])

    await async_engine.save_all([obj_db_0, obj_db_1])
    query_0 = (ModelMain.attr_3.attr_1 == "one") & (ModelMain.attr_3.attr_2 == "two")
    result_0 = await async_engine.find_many(Model=ModelMain, query=query_0)
    query_1 = elem_match(
        ModelEmbedded.attr_1 == "one",
        ModelEmbedded.attr_2 == "two",
        field=ModelMain.attr_3,
    )
    result_1 = await async_engine.find_many(Model=ModelMain, query=query_1)
    assert len(result_0) == 2
    assert len(result_1) == 1
