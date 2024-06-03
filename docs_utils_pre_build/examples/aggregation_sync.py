from pyodmongo import DbModel, DbEngine, Id
from typing import ClassVar

engine = DbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


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


result: list[OrdersByCustomers] = engine.find_many(Model=OrdersByCustomers)
