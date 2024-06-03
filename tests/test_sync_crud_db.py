from pyodmongo import (
    DbEngine,
    DbModel,
    Id,
    DbResponse,
    ResponsePaginate,
    Field,
)
from pyodmongo.queries import eq, gte, gt, sort
from pyodmongo.engines.utils import consolidate_dict
from pydantic import ConfigDict
from typing import ClassVar
from bson import ObjectId
from datetime import datetime, UTC, timezone, timedelta
import pytz
import pytest

mongo_uri = "mongodb://localhost:27017"
db_name = "pyodmongo_pytest"
db = DbEngine(
    mongo_uri=mongo_uri, db_name=db_name, tz_info=pytz.timezone("America/Sao_Paulo")
)


class MyClass(DbModel):
    attr1: str
    attr2: str
    random_number: int | None = None
    _collection: ClassVar = "my_class_test"


@pytest.fixture()
def drop_collection():
    db._db[MyClass._collection].drop()
    yield MyClass(attr1="attr_1", attr2="attr_2")
    db._db[MyClass._collection].drop()


@pytest.fixture()
def create_100_docs_in_db():
    obj_list = []
    for n in range(1, 101):
        obj_list.append(MyClass(attr1="Value 1", attr2="Value 2", random_number=n))
    db.save_all(obj_list)


@pytest.fixture()
def new_obj():
    yield MyClass(attr1="attr_1", attr2="attr_2")


def test_check_if_create_a_new_doc_on_save(drop_collection, new_obj):
    result: DbResponse = db.save(new_obj)
    assert ObjectId.is_valid(result.upserted_ids[0])
    assert new_obj.id == result.upserted_ids[0]
    assert isinstance(new_obj.created_at, datetime)
    assert isinstance(new_obj.updated_at, datetime)
    assert new_obj.created_at == new_obj.updated_at


def test_create_and_delete_one(drop_collection, new_obj):
    result: DbResponse = db.save(new_obj)
    assert result.upserted_ids[0] is not None
    id = result.upserted_ids[0]
    query = eq(MyClass.id, id)
    result: DbResponse = db.delete(Model=MyClass, query=query, delete_one=True)
    assert result.deleted_count == 1


def test_find_one(drop_collection, new_obj):
    result: DbResponse = db.save(new_obj)
    id_returned = result.upserted_ids[0]
    obj_found = db.find_one(MyClass, eq(MyClass.id, id_returned))

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


def test_save_all_created(drop_collection, objs):
    db.save_all(objs)
    assert all([ObjectId.is_valid(obj.id) for obj in objs])


def test_update_on_save(drop_collection, objs):
    db.save_all(objs)
    obj = MyClass(attr1="value_1", attr2="value_2")
    response: DbResponse = db.save(obj, eq(MyClass.attr1, "attr_3"))

    assert response.matched_count == 2
    assert response.modified_count == 2
    assert response.upserted_ids == {}


def test_delete(drop_collection, objs):
    db.save_all(objs)
    response: DbResponse = db.delete(MyClass, eq(MyClass.attr1, "attr_1"))
    assert response.deleted_count == 3


def test_find_many_without_paginate(drop_collection, create_100_docs_in_db):
    obj_list_50 = db.find_many(Model=MyClass, query=gt(MyClass.random_number, 50))
    obj_list_100 = db.find_many(Model=MyClass, query=gt(MyClass.random_number, 0))
    assert len(obj_list_50) == 50
    assert len(obj_list_100) == 100
    assert all(isinstance(obj, MyClass) for obj in obj_list_100)


def test_find_many_with_paginate(drop_collection, create_100_docs_in_db):
    response_paginate: ResponsePaginate = db.find_many(
        Model=MyClass,
        query=gt(MyClass.random_number, 50),
        paginate=True,
        docs_per_page=10,
    )
    assert isinstance(response_paginate, ResponsePaginate)
    assert response_paginate.docs_quantity == 50
    assert len(response_paginate.docs) == 10


def test_with_query_and_raw_query_none(drop_collection, create_100_docs_in_db):
    all_obj = db.find_many(Model=MyClass)
    assert len(all_obj) == 100


def test_field_alias():
    class MyClass(DbModel):
        first_name: str = Field(alias="firstName", default=None)
        second_name: str = Field(alias="secondName", default=None)
        third_name: str = None
        _collection: ClassVar = "alias_test"

    db._db[MyClass._collection].drop()

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
    db.save(obj)
    obj_found = db.find_one(Model=MyClass)
    assert obj == obj_found

    db._db[MyClass._collection].drop()


def test_fields_alias_generator():
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

    db._db[MyClass._collection].drop()

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
    db.save(obj)
    obj_found = db.find_one(Model=MyClass)
    assert obj == obj_found
    db._db[MyClass._collection].drop()


def test_find_many_with_zero_results(drop_collection):
    db.save(obj=drop_collection)
    result = db.find_many(
        Model=MyClass, query=eq(MyClass.attr1, "value_that_not_exists"), paginate=True
    )

    assert result.page_quantity == 0
    assert result.docs_quantity == 0
    assert result.docs == []


def test_find_one_with_zero_results(drop_collection):
    db.save(obj=drop_collection)
    result = db.find_one(
        Model=MyClass, query=eq(MyClass.attr1, "value_that_not_exists")
    )

    assert result is None


def test_delete_one_type_error_when_query_is_not_comparison_or_logical_operator():
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        db.delete(Model=MyClass, query="string", delete_one=True)


def test_delete_type_error_when_query_is_not_comparison_or_logical_operator():
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        db.delete(Model=MyClass, query="string")


def test_save_type_error_when_query_is_not_comparison_or_logical_operator(
    drop_collection,
):
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        db.save(obj=drop_collection, query="string")


def test_find_one_type_error_when_query_is_not_comparison_or_logical_operator():
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        db.find_one(Model=MyClass, query="string")


def test_find_many_type_error_when_query_is_not_comparison_or_logical_operator():
    with pytest.raises(
        TypeError,
        match='query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument',
    ):
        db.find_many(Model=MyClass, query="string")


def test_find_with_populate():
    class MyModel1(DbModel):
        attr1: str
        _collection: ClassVar = "model1"

    class MyModel2(DbModel):
        attr2: str
        my_model_1: MyModel1 | Id
        _collection: ClassVar = "model2"

    db._db[MyModel1._collection].drop()
    db._db[MyModel2._collection].drop()

    obj_1 = MyModel1(attr1="attr_1")
    db.save(obj_1)
    obj_2 = MyModel2(attr2="attr_2", my_model_1=obj_1)
    db.save(obj_2)

    obj_found = db.find_one(Model=MyModel2, populate=True)
    assert obj_found == obj_2
    db._db[MyModel1._collection].drop()
    db._db[MyModel2._collection].drop()


def test_find_without_populate():
    class MyModel1(DbModel):
        attr1: str
        _collection: ClassVar = "model1"

    class MyModel2(DbModel):
        attr2: str
        my_model_1: MyModel1 | Id
        _collection: ClassVar = "model2"

    db._db[MyModel1._collection].drop()
    db._db[MyModel2._collection].drop()

    obj_1 = MyModel1(attr1="attr_1")
    db.save(obj_1)
    obj_2 = MyModel2(attr2="attr_2", my_model_1=obj_1.id)
    db.save(obj_2)

    obj_found = db.find_one(Model=MyModel2)
    assert obj_found == obj_2

    db._db[MyModel1._collection].drop()
    db._db[MyModel2._collection].drop()


class AsDict1(DbModel):
    attr_1: str
    _collection: ClassVar = "as_dict_1"


class AsDict2(DbModel):
    attr_2: str
    as_dict_1: list[AsDict1 | Id]
    _collection: ClassVar = "as_dict_2"


@pytest.fixture
def create_find_dict_collection():
    db._db[AsDict1._collection].drop()
    db._db[AsDict2._collection].drop()

    obj1 = AsDict1(attr_1="Obj 1")
    obj2 = AsDict1(attr_1="Obj 2")
    db.save_all([obj1, obj2])
    obj3 = AsDict2(attr_2="Obj 3", as_dict_1=[obj1, obj2])
    obj4 = AsDict2(attr_2="Obj 4", as_dict_1=[obj2, obj1])
    obj5 = AsDict2(attr_2="Obj 4", as_dict_1=[obj2, obj1])
    obj6 = AsDict2(attr_2="Obj 4", as_dict_1=[obj2, obj1])
    db.save_all([obj3, obj4, obj5, obj6])

    yield
    db._db[AsDict1._collection].drop()
    db._db[AsDict2._collection].drop()


def test_find_as_dict(create_find_dict_collection):
    obj_list = db.find_many(Model=AsDict2, as_dict=True, populate=True)
    assert len(obj_list) == 4
    assert type(obj_list) is list
    for dct in obj_list:
        assert type(dct) == dict
    obj_dict = db.find_one(Model=AsDict2, as_dict=True, populate=True)
    assert type(obj_dict) == dict


class MySortClass(DbModel):
    attr_1: str
    attr_2: int
    attr_3: datetime
    _collection: ClassVar = "my_class_to_sort"


@pytest.fixture()
def drop_collection_for_test_sort():
    db._db[MySortClass._collection].drop()
    yield
    db._db[MySortClass._collection].drop()


def test_sort_query(drop_collection_for_test_sort):
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
    db.save_all(obj_list=obj_list)
    sort_oprator = sort((MySortClass.attr_1, 1), (MySortClass.attr_2, 1))
    result_many = db.find_many(Model=MySortClass, sort=sort_oprator)
    assert result_many[0] == obj_list[4]
    assert result_many[1] == obj_list[1]

    sort_oprator = sort((MySortClass.attr_3, 1))
    result_one = db.find_one(Model=MySortClass, sort=sort_oprator)
    assert result_one == obj_list[2]

    sort_oprator = ["attr_3", 1]
    with pytest.raises(
        TypeError,
        match='sort argument must be a SortOperator from pyodmongo.queries. If you really need to make a very specific sort, use "raw_sort" argument',
    ):
        result_one = db.find_one(Model=MySortClass, sort=sort_oprator)

    with pytest.raises(
        TypeError,
        match='sort argument must be a SortOperator from pyodmongo.queries. If you really need to make a very specific sort, use "raw_sort" argument',
    ):
        result_many = db.find_many(Model=MySortClass, sort=sort_oprator)


class ClassWithDate(DbModel):
    name: str
    date: datetime
    _collection: ClassVar = "class_with_date"


@pytest.fixture()
def drop_collection_class_with_date():
    db._db[ClassWithDate._collection].drop()
    yield
    db._db[ClassWithDate._collection].drop()


def test_save_and_retrieve_objs_with_datetime(drop_collection_class_with_date):
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
    db.save(obj)
    query = (ClassWithDate.date >= datetime(2024, 4, 24, 22, 30, 0, tzinfo=tz)) & (
        ClassWithDate.date <= datetime(2024, 4, 24, 23, 30, 0, tzinfo=tz)
    )
    obj_found: ClassWithDate = db.find_one(Model=ClassWithDate, query=query)
    assert obj_found.date == date
