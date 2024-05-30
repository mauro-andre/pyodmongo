# <center>Query</center>

Creating queries in **PyODMongo** is straightforward and intuitive. It simplifies the process of building MongoDB queries, providing a Pythonic and straightforward approach to working with **Comparison Operators** and **Logical Operators** found in MongoDB.

In **PyODMongo**, a query serves as an essential attribute of the `find_many` and `find_one` methods, which are available through the `DbEngine` and `AsyncDbEngine` classes. These methods empower you to retrieve data from your MongoDB database with ease, combining the simplicity of Python with the robust querying capabilities of MongoDB.

## Comparison Operators

| Operator | Usage |
| ---------|--- |
| **EQ**  | `eq(Model.attr, value)`</br>`Model.attr == value` |
| **GT**   | `gt(Model.attr, value)`</br>`Model.attr > value` |
| **GTE** | `gte(Model.attr, value)`</br>`Model.attr >= value` |
| **IN**        | `in_(Model.attr, value)` |
| **LT**   | `lt(Model.attr, value)`</br>`Model.attr < value` |
| **LTE** | `lte(Model.attr, value)`</br>`Model.attr <= value` |
| **NE**  | `ne(Model.attr, value)`</br>`Model.attr != value` |
| **NIN**            | `nin(Model.attr, value)` |


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
    query =  Product.price >= 5
    #query = gte(Product.price, 5)
    sort_oprator = sort((Product.name, 1), (Product.price, -1))
    result: Product = await engine.find_one(Model=Product, query=query, sort=sort_oprator)

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


query = Product.price >= 5
#query = gte(Product.price, 5)
sort_oprator = sort((Product.name, 1), (Product.price, -1))
result: Product = engine.find_one(Model=Product, query=query, sort=sort_oprator)
```
///

In this example, the query will return all documents  in 'products' collection where the 'price' field is equal to or greater than 5.

## Logical Operators

Just like Comparison Operators, Logical Operators in **PyODMongo** are designed to mirror their counterparts in MongoDB itself.

Here are the primary Logical Operators available in PyODMongo:

| Operator | Usage |
| ---------|-|
| **AND**| `and_(gt(Model.attr_1, value_1), lt(Model.attr_1, value_2))`</br>`(Model.attr_1 > value_1) & (Model.attr_1 < value_2)` |
| **OR** | `or_(eq(Model.attr_1, value_1), eq(Model.attr_1, value_2))`</br>`(Model.attr_1 == value_1) | (Model.attr_1 == value_2)` |
| **NOR** | `nor(Model.attr_1 == value_1, Model.attr_1 == value_2)` |


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
    query = (Product.is_available == True) & (Product.price >= 5)
    # query = and_(
    #     eq(Product.is_available, True),
    #     gte(Product.price, 5)
    # )
    sort_oprator = sort((Product.name, 1), (Product.price, -1))
    result: Product = await engine.find_one(Model=Product, query=query, sort=sort_oprator)

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


query = (Product.is_available == True) & (Product.price >= 5)
# query = and_(
#     eq(Product.is_available, True),
#     gte(Product.price, 5)
# )
sort_oprator = sort((Product.name, 1), (Product.price, -1))
result: Product = engine.find_one(Model=Product, query=query, sort=sort_oprator)

```
///

In this example, the query returns all documents from the 'products' collection that `is_available` is `True` and that have `price` greater than or equal to 5

!!! tip
    The inputs for these Logical Operators can be Comparison Operators or even other Logical Operators. This flexibility allows you to create complex and nested queries, enabling you to express intricate data retrieval conditions with precision.

## Sort

/// tab | Async
```python hl_lines="19"
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
    query = Product.price >= 5
    sort_oprator = sort((Product.name, 1), (Product.price, -1))
    result: Product = await engine.find_one(Model=Product, query=query, sort=sort_oprator)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="17"
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


query = Product.price >= 5
sort_oprator = sort((Product.name, 1), (Product.price, -1))
result: Product = engine.find_one(Model=Product, query=query, sort=sort_oprator)
```
///

In the provided example, the `sort_operator` is defined using the `sort` function, which takes tuples. Each tuple contains two elements: the first one is the field by which you want to sort, and the second one is the sorting direction, where 1 indicates ascending order and -1 indicates descending order. In the presented case, the `sort_operator` sorts the results first by the name field in ascending order and then by the price field in descending order. Thus, the products are returned in alphabetical order by name and, in case of a tie, in descending order by price.