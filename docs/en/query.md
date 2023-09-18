# <center>Query</center>

Creating queries in **PyODMongo** is straightforward and intuitive. It simplifies the process of building MongoDB queries, providing a Pythonic and straightforward approach to working with **Comparison Operators** and **Logical Operators** found in MongoDB.

In **PyODMongo**, a query serves as an essential attribute of the `find_many` and `find_one` methods, which are available through the `DbEngine` and `AsyncDbEngine` classes. These methods empower you to retrieve data from your MongoDB database with ease, combining the simplicity of Python with the robust querying capabilities of MongoDB.

## Comparison Operators

| Operator | Description                          |
| ---------| ------------------------------------ |
| `eq`     | Matches values that are equal to a specified value.  |
| `gt`     | Matches values that are greater than a specified value. |
| `gte`    | Matches values that are greater than or equal to a specified value. |
| `in_`    | Matches any of the values specified in an list. |
| `lt`     | Matches values that are less than a specified value. |
| `lte`    | Matches values that are less than or equal to a specified value. |
| `ne`     | Matches all values that are not equal to a specified value. |
| `nin`    | Matches none of the values specified in an list. |


When using these Comparison Operators in PyODMongo, you'll typically provide two arguments:

- `field: DbField`: This argument represents the field of your PyODMongo `DbModel` class that you want to search in the database. It defines the property you want to apply the comparison operator to.

- `value: Any`: This argument specifies the value you want to compare against the field defined in the first argument. It represents the reference value to be found in the database.

Here's an example of how to use a Comparison Operator in PyODMongo:

/// tab | Async
```python hl_lines="18"
from pyodmongo import AsyncDbEngine, DbModel
from pyodmongo.queries import ( eq, gt, gte, in_, lt, lte, ne, nin, text, 
                                and_, or_, nor)
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


async def main():
    query = gte(Product.price, 5)
    result: Product = await engine.find_one(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="16"
from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import ( eq, gt, gte, in_, lt, lte, ne, nin, text, 
                                and_, or_, nor)
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


query = gte(Product.price, 5)
result: Product = engine.find_one(Model=Product, query=query)
```
///

In this example, the query will return all documents  in 'products' collection where the 'price' field is equal to or greater than 5.

## Logical Operators

Just like Comparison Operators, Logical Operators in **PyODMongo** are designed to mirror their counterparts in MongoDB itself.

Here are the primary Logical Operators available in PyODMongo:

| Operator | Description                          |
| ---------| ------------------------------------ |
| `and_` | Join query clauses with a logical **AND**. Returns all documents that match the conditions of all clauses. |
| `or_` | Join query clauses with a logical **OR**. Returns all documents that match the conditions of any of the clauses. |
| `nor` | Join query clauses with a logical **NOR**. Returns the inverse of **OR** |


Here's an example of how you can use Logical Operators in PyODMongo:

/// tab | Async
```python hl_lines="18"
from pyodmongo import AsyncDbEngine, DbModel
from pyodmongo.queries import (eq, gt, gte, in_, lt, lte, ne, nin, text,
                               and_, or_, nor)
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


async def main():
    query = and_(
        eq(Product.is_available, True),
        gte(Product.price, 5)
    )
    result: Product = await engine.find_one(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="17"
from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import (eq, gt, gte, in_, lt, lte, ne, nin, text,
                               and_, or_, nor)
from typing import ClassVar
import asyncio

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


query = and_(
    eq(Product.is_available, True),
    gte(Product.price, 5)
)
result: Product = engine.find_one(Model=Product, query=query)

```
///

In this example, the query returns all documents from the 'products' collection that `is_available` is `True` and that have `price` greater than or equal to 5

!!! tip
    The inputs for these Logical Operators can be Comparison Operators or even other Logical Operators. This flexibility allows you to create complex and nested queries, enabling you to express intricate data retrieval conditions with precision.