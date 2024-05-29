from pyodmongo import DbModel, AsyncDbEngine, Id
from typing import ClassVar
import pytest_asyncio
import pytest


class Customer(DbModel):
    name: str
    email: str
    _collection: ClassVar = "customers"


class Order(DbModel):
    customer: Customer | Id
    value: float
    _collection: ClassVar = "orders"


class OrdersByCustomers(DbModel):
    count: int
    total_value: float
    _collection: ClassVar = "orders"
    _pipeline: ClassVar = [
        {
            "$group": {
                "_id": "$customer",
                "count": {"$count": {}},
                "total_value": {"$sum": "$value"},
            }
        }
    ]


@pytest_asyncio.fixture()
async def drop_collections(async_engine):
    await async_engine._db[Customer._collection].drop()
    await async_engine._db[Order._collection].drop()
    yield
    await async_engine._db[Customer._collection].drop()
    await async_engine._db[Order._collection].drop()


@pytest.mark.asyncio
async def test_pipeline_aggregate(drop_collections, async_engine):
    customer_1 = Customer(name="Customer 1", email="customer1@email.com")
    customer_2 = Customer(name="Customer 2", email="customer2@email.com")
    customer_3 = Customer(name="Customer 3", email="customer3@email.com")
    await async_engine.save_all([customer_1, customer_2, customer_3])
    for n in range(1, 11):
        await async_engine.save(Order(customer=customer_1, value=n))
    for n in range(1, 5):
        await async_engine.save(Order(customer=customer_2, value=n))
    for n in range(1, 8):
        await async_engine.save(Order(customer=customer_3, value=n))

    objs = await async_engine.find_many(Model=OrdersByCustomers)
    customer_1_aggregate: OrdersByCustomers = list(
        filter(lambda x: x.id == customer_1.id, objs)
    )[0]
    customer_2_aggregate: OrdersByCustomers = list(
        filter(lambda x: x.id == customer_2.id, objs)
    )[0]
    customer_3_aggregate: OrdersByCustomers = list(
        filter(lambda x: x.id == customer_3.id, objs)
    )[0]

    assert customer_1_aggregate.count == 10
    assert customer_1_aggregate.total_value == 55
    assert customer_2_aggregate.count == 4
    assert customer_2_aggregate.total_value == 10
    assert customer_3_aggregate.count == 7
    assert customer_3_aggregate.total_value == 28
