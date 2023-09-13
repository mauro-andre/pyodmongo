# <center>Getting Started</center>


In this guide, we'll walk you through the initial steps to get started with **PyODMongo**, a Python MongoDB Object-Document Mapper (ODM). We'll cover creating the engine, defining a model, saving data, and reading from the database.

## Creating the Engine

To begin using **PyODMongo**, you first need to create an instance of the `AsyncDbEngine` or `DbEngine` class to connect to your MongoDB server. Here's how you can do it:

/// tab | Async
```python hl_lines="5"
from pyodmongo import AsyncDbEngine, DbModel
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)


async def main():
    result = await engine.save(box)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="4"
from pyodmongo import DbEngine, DbModel
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)

result = engine.save(box)
```
///

Make sure to replace `mongodb://localhost:27017` with the connection string to your MongoDB database and `my_db` with de database name.

## Defining a Model
Next, you'll define a model that inherits from DbModel. This model represents the structure of your MongoDB documents. You'll also need to create the `_collection` attribute, which will carry the collection name string to be saved in the database.

/// tab | Async
```python hl_lines="8 12"
from pyodmongo import AsyncDbEngine, DbModel
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)


async def main():
    result = await engine.save(box)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="7 11"
from pyodmongo import DbEngine, DbModel
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)

result = engine.save(box)
```
///

In this example, we've created a `Product` class, that inherits from `DbModel`, to define the structure of our MongoDB documents.

## Saving Data
You can save data to the MongoDB database using the `save()` method of your `AsyncDbEngine` or `DbEngine` instance.

/// tab | Async
```python hl_lines="19"
from pyodmongo import AsyncDbEngine, DbModel
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)


async def main():
    result = await engine.save(box)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="16"
from pyodmongo import DbEngine, DbModel
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)

result = engine.save(box)
```
///

This code creates a new document using the data provided, and then it is saved to the MongoDB database.

## Reading from the Database
To read data from the database, you can use the `find_one()` method of your `AsyncDbEngine` or `DbEngine` instance.

/// tab | Async
```python hl_lines="18"
from pyodmongo import AsyncDbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


async def main():
    query = eq(Product.name, 'Box')
    box: Product = await engine.find_one(Model=Product, query=query)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="16"
from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


query = eq(Product.name, 'Box')
box: Product = engine.find_one(Model=Product, query=query)
```
///

This code queries the database for a product with name 'Box' and creates a `Product` type object with the document found in database.

These are the first steps to get you started with **PyODMongo**. You can now create, save, and read data from your MongoDB database using this Python MongoDB Object-Document Mapper.