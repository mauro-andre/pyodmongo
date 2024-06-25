from typing import ClassVar
import pytest
import pytest_asyncio
from pyodmongo import (
    AsyncDbEngine,
    DbEngine,
    DbModel,
    MainBaseModel,
    DbResponse,
    ResponsePaginate,
    Id,
    Field,
)
from pydantic import BaseModel
from bson import ObjectId
import copy
from faker import Faker


fake = Faker()


@pytest_asyncio.fixture
async def drop_db(async_engine: AsyncDbEngine, engine: DbEngine):
    await async_engine._client.drop_database("pyodmongo_pytest")
    engine._client.drop_database("pyodmongo_pytest")
    yield
    await async_engine._client.drop_database("pyodmongo_pytest")
    engine._client.drop_database("pyodmongo_pytest")


@pytest.mark.asyncio
async def test_save_all(async_engine: AsyncDbEngine, engine: DbEngine):
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

    response_0: dict[str, DbResponse] = await async_engine.save_all([obj_0, obj_2])
    response_1: dict[str, DbResponse] = engine.save_all([obj_1, obj_3])

    assert response_0["my_class_0"].upserted_count == 1
    assert response_0["my_class_0"].upserted_ids[0] == obj_0.id
    assert response_0["my_class_1"].upserted_count == 1
    assert response_0["my_class_1"].upserted_ids[0] == obj_2.id
    assert response_1["my_class_0"].upserted_count == 1
    assert response_1["my_class_0"].upserted_ids[0] == obj_1.id
    assert response_1["my_class_1"].upserted_count == 1
    assert response_1["my_class_1"].upserted_ids[0] == obj_3.id

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
async def test_save(async_engine: AsyncDbEngine, engine: DbEngine, drop_db):
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
async def test_find(async_engine: AsyncDbEngine, engine: DbEngine, drop_db):
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

    obj_found_0_49 = await async_engine.find_one(
        Model=MyClass0, query=MyClass0.id == obj_to_find_0_49.id
    )
    obj_found_50_49 = engine.find_one(
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


@pytest.mark.asyncio
async def test_delete(async_engine: AsyncDbEngine, engine: DbEngine, drop_db):
    class MyClass0(DbModel):
        attr_0: str = Field(index=True)
        attr_1: int = Field(index=True)
        _collection: ClassVar = "my_class_0"

    objs_0_49 = [MyClass0(attr_0=fake.name(), attr_1=n) for n in range(0, 50)]
    objs_50_99 = [MyClass0(attr_0=fake.name(), attr_1=n) for n in range(50, 100)]

    await async_engine.save_all(objs_0_49)
    engine.save_all(objs_50_99)

    query_0 = (MyClass0.attr_1 >= 0) & (MyClass0.attr_1 < 10)
    query_1 = (MyClass0.attr_1 >= 50) & (MyClass0.attr_1 < 60)

    response_0: DbResponse = await async_engine.delete(
        Model=MyClass0, query=query_0, delete_one=True
    )
    response_1: DbResponse = engine.delete(
        Model=MyClass0, query=query_1, delete_one=True
    )
    assert response_0.deleted_count == 1
    assert response_1.deleted_count == 1

    find_result_0 = await async_engine.find_many(Model=MyClass0)
    find_result_1 = engine.find_many(Model=MyClass0)
    assert len(find_result_0) == 98
    assert len(find_result_1) == 98

    response_0: DbResponse = await async_engine.delete(Model=MyClass0, query=query_0)
    response_1: DbResponse = engine.delete(Model=MyClass0, query=query_1)
    assert response_0.deleted_count == 9
    assert response_1.deleted_count == 9

    find_result_0 = await async_engine.find_many(Model=MyClass0)
    find_result_1 = engine.find_many(Model=MyClass0)

    assert len(find_result_0) == 80
    assert len(find_result_1) == 80


@pytest.mark.asyncio
async def test_db_field_population(
    async_engine: AsyncDbEngine, engine: DbEngine, drop_db
):
    class MyClassA(DbModel):
        attr_a_1: str
        attr_a_2: str
        _collection: ClassVar = "my_class_a"

    class MyClassB(DbModel):
        attr_b_1: str
        attr_obj_a: MyClassA | Id
        _collection: ClassVar = "my_class_b"

    class MyClassC(DbModel):
        attr_c_1: str
        attr_obj_b: MyClassB | Id
        _collection: ClassVar = "my_class_c"

    obj_a = MyClassA(attr_a_1="value_a_1", attr_a_2="value_a_2")
    engine.save(obj_a)
    obj_b = MyClassB(attr_b_1="value_b_1", attr_obj_a=obj_a)
    await async_engine.save(obj_b)
    obj_c = MyClassC(attr_c_1="value_c_1", attr_obj_b=obj_b)
    await async_engine.save(obj_c)

    populate_db_fields = [MyClassC.attr_obj_b]
    obj_found = await async_engine.find_one(
        Model=MyClassC, populate=True, populate_db_fields=populate_db_fields
    )
    obj_c.attr_obj_b.attr_obj_a = obj_a.id
    assert obj_found == obj_c


@pytest.mark.asyncio
async def test_error_save_base_model(
    async_engine: AsyncDbEngine, engine: DbEngine, drop_db
):
    class MyClassA(BaseModel):
        a1: str = "a1"

    class MyClassB(DbModel):
        b1: str = "b1"
        obj_a: MyClassA = MyClassA()
        _collection: ClassVar = "my_class_b"

    obj = MyClassB()

    with pytest.raises(
        TypeError,
        match="The MyClassA class inherits from Pydantic's BaseModel class. Try switching to PyODMongo's MainBaseModel class",
    ):
        await async_engine.save(obj)

    with pytest.raises(
        TypeError,
        match="The MyClassA class inherits from Pydantic's BaseModel class. Try switching to PyODMongo's MainBaseModel class",
    ):
        engine.save(obj)


@pytest.mark.asyncio
async def test_list_of_empty_objects(
    async_engine: AsyncDbEngine, engine: DbEngine, drop_db
):
    class A(DbModel):
        name: str = "A Name"
        code: str = "A Code"
        _collection: ClassVar = "a"

    class B(MainBaseModel):
        a: A | Id
        code: str = "B Code"
        cost: float = 100

    class C(DbModel):
        name: str = "name_1"
        b_list: list[B] | None = None
        _collection: ClassVar = "c"

    obj_c = C()
    engine.save(obj_c)
    obj_found = await async_engine.find_one(Model=C, populate=True)
    assert obj_found == obj_c


@pytest.mark.asyncio
async def test_field_population_with_main_base_model(
    async_engine: AsyncDbEngine, engine: DbEngine, drop_db
):
    class S(DbModel):
        s1: str = "s1"
        _collection: ClassVar = "s"

    class BC(DbModel):
        b1: str = "b1"
        s: S | Id
        _collection: ClassVar = "bc"

    class A(MainBaseModel):
        a1: str = "a1"
        bc: BC | Id

    class P(DbModel):
        p1: str = "p1"
        a: A
        _collection: ClassVar = "p"

    class O(DbModel):
        o1: str = "o1"
        p: P | Id
        _collection: ClassVar = "o"

    obj_s = S()
    await async_engine.save(obj_s)
    obj_bc = BC(s=obj_s)
    await async_engine.save(obj_bc)
    obj_a = A(bc=obj_bc)
    obj_p = P(a=obj_a)
    engine.save(obj_p)
    obj_o = O(p=obj_p)
    engine.save(obj_o)

    obj_found = engine.find_one(
        Model=O, populate=True, populate_db_fields=[O.p, A.bc, BC.s]
    )
    assert obj_found == obj_o
