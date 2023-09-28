from pyodmongo import DbModel, AsyncDbEngine, Id
from typing import ClassVar
import pytest_asyncio
import pytest

mongo_uri = "mongodb://localhost:27017"
db_name = "pyodmongo_pytest"
engine = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name)


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
async def drop_collections():
    await engine._db[Customer._collection].drop()
    await engine._db[Order._collection].drop()
    yield
    await engine._db[Customer._collection].drop()
    await engine._db[Order._collection].drop()


@pytest.mark.asyncio
async def test_pipeline_aggregate(drop_collections):
    customer_1 = Customer(name="Customer 1", email="customer1@email.com")
    customer_2 = Customer(name="Customer 2", email="customer2@email.com")
    customer_3 = Customer(name="Customer 3", email="customer3@email.com")
    await engine.save_all([customer_1, customer_2, customer_3])
    for n in range(1, 11):
        await engine.save(Order(customer=customer_1, value=n))
    for n in range(1, 5):
        await engine.save(Order(customer=customer_2, value=n))
    for n in range(1, 8):
        await engine.save(Order(customer=customer_3, value=n))

    objs = await engine.find_many(Model=OrdersByCustomers)
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
