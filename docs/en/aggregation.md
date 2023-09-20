# <center>Aggregation</center>

Aggregation is a fantastic feature of MongoDB that allows you to perform various data transformations and analysis. Although MongoDB's Aggregation Pipeline is a powerful tool, it can sometimes be complex to work with due to its stages and expressions, but once you master the tool, it becomes a powerful ally in data analysis.

At **PyODMongo**, we offer you the ability to leverage the full power of the MongoDB aggregation framework and to use it you need to be familiar with this feature.

To utilize the capabilities of aggregation in **PyODMongo**, you can insert aggregation pipelines directly into your models. All you need to do is create a class-level attribute named `_pipeline` in your model and defining the aggregation stages. When you use the `find_one` or `find_many` methods in **PyODMongo**, the library will execute the aggregation pipeline and return the result as Python objects.

Here's a simple example using just the `$group` stage from the MongoDB Aggregation Pipeline:

/// tab | Async
```python
from pyodmongo import DbModel, AsyncDbEngine, Id
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Customer(DbModel):
    name: str
    email: str
    _collection: ClassVar = 'customers'


class Order(DbModel):
    customer: Customer | Id
    value: float
    _collection: ClassVar = 'orders'


class OrdersByCustomers(DbModel):
    count: int
    total_value: float
    _collection: ClassVar = 'orders'
    _pipeline: ClassVar = [
        {
            '$group': {
                '_id': '$customer',
                'count': {'$count': {}},
                'total_value': {'$sum': '$value'},
            }
        }
    ]


async def main():
    result: list[OrdersByCustomers] = await engine.find_many(Model=OrdersByCustomers)

asyncio.run(main())
```
///
/// tab | Sync
```python
from pyodmongo import DbModel, DbEngine, Id
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Customer(DbModel):
    name: str
    email: str
    _collection: ClassVar = 'customers'


class Order(DbModel):
    customer: Customer | Id
    value: float
    _collection: ClassVar = 'orders'


class OrdersByCustomers(DbModel):
    count: int
    total_value: float
    _collection: ClassVar = 'orders'
    _pipeline: ClassVar = [
        {
            '$group': {
                '_id': '$customer',
                'count': {'$count': {}},
                'total_value': {'$sum': '$value'},
            }
        }
    ]


result: list[OrdersByCustomers] = engine.find_many(Model=OrdersByCustomers)
```
///

In this example, we have an `OrdersByCustomers` model with an aggregation pipeline that groups orders by customer, calculating the count of orders and the total order value for each customer.

**PyODMongo** provides flexibility in using aggregation, but it's essential to ensure that the aggregation output aligns with the fields defined in your class to avoid errors when instantiating objects.

With PyODMongo's aggregation support, you can unlock the full potential of MongoDB's data transformation capabilities while maintaining a Pythonic and intuitive coding experience. The possibilities for data analysis and processing are virtually limitless.