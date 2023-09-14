# <center>Save</center>

## Save

The `save` method is a part of the `AsyncDbEngine` and `DbEngine` classes in **PyODMongo**. It is responsible for saving or updating documents in the database.

/// tab | Async
```python hl_lines="19"
from pyodmongo import AsyncDbEngine, DbModel, SaveResponse
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
    result: SaveResponse = await engine.save(box)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="16"
from pyodmongo import DbEngine, DbModel, SaveResponse
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)

result: SaveResponse = engine.save(box)
```
///

If the result of the `save` method corresponds to the creation of a new document in the database, the object instance will receive the `id`, `created_at`, and `updated_at` attributes.

## Arguments

- `obj: Any`: The object to be saved in the database.
- `query: ComparisonOperator | LogicalOperator = None`: A query used to update matching documents. If not provided, the document in the database with `_id` equals to `obj.id` will be updated. If `obj` does not have an `id`, a new document will be created in the database.
- `raw_query: dict = None`: A query in the format accepted by MongoDB. This parameter allows you to specify a custom query for updating documents.

!!! warning
    If `raw_query` is passed, `query` will not be considered.

!!! note
    Under the hood, **PyODMongo** uses the `update_many` operation with `upsert=True`, which means it can add or update one or multiple documents.


## Save all

In addition to the `save` method, **PyODMongo** provides the `save_all` method, which enables you to save a list of objects. This method is particularly useful when you need to save multiple documents.

/// tab | Async
```python hl_lines="22"
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


class User(DbModel):
    name: str
    email: str
    password: str
    _collection: ClassVar = 'users'


obj_list = [
    Product(name='Box', price='5.99', is_available=True),
    Product(name='Ball', price='6.99', is_available=True),
    User(name='John', email='john@email.com', password='john_pwd')
]

async def main():
    result: list[SaveResponse] = await engine.save_all(obj_list)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="21"
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


class User(DbModel):
    name: str
    email: str
    password: str
    _collection: ClassVar = 'users'


obj_list = [
    Product(name='Box', price='5.99', is_available=True),
    Product(name='Ball', price='6.99', is_available=True),
    User(name='John', email='john@email.com', password='john_pwd')
]

result: list[SaveResponse] = engine.save_all(obj_list)
```
///

## Save response

The `save` method in **PyODMongo** returns a `SaveResponse` object that provides information about the outcome of the save operation. This object contains several attributes that give insights into how the save operation affected the database.

### Attributes

- `acknowledged`: A boolean value indicating whether the operation was acknowledged by the MongoDB server. If the operation was acknowledged, this attribute is set to `True`, indicating that the server recognized and processed the save request.

- `matched_count`: An integer that represents the number of documents in the database that matched the query or criteria specified during the save operation. This count indicates how many existing documents were updated as part of the save operation.

- `modified_count`: An integer that represents the number of documents in the database that were actually modified during the save operation. This count is usually the same as or a subset of the `matched_count` and indicates how many documents had their fields changed.

- `upserted_id`: If the save operation resulted in the insertion of a new document (upsert), this attribute holds the `_id` of the newly inserted document. When no upsert occurs, this attribute is `None`.

- `raw_result`: A dictionary containing the raw result of the MongoDB save operation. This dictionary may contain additional information provided by the MongoDB server, and its structure can vary based on the specific MongoDB driver and version.