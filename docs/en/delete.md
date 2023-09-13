# <center>Delete</center>

## Delete

The `delete` method is available in both `AsyncDbEngine` and `DbEngine` and is used to delete documents from a MongoDB collection based on a specified query. This method offers a straightforward way to remove documents that match specific criteria from your MongoDB database.

/// tab | Async
```python hl_lines="21"
from pyodmongo import AsyncDbEngine, DbModel, DeleteResponse
from pyodmongo.queries import eq
from typing import ClassVar
import asyncio

# Initialize the database engine
engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

# Define a model
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

async def main():
    # Define a query to specify which documents to delete
    query = eq(Product.name, 'Box')

    # Use the delete method to remove documents
    result: DeleteResponse = await engine.delete(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="19"
from pyodmongo import DbEngine, DbModel, DeleteResponse
from pyodmongo.queries import eq
from typing import ClassVar

# Initialize the database engine
engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

# Define a model
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

# Define a query to specify which documents to delete
query = eq(Product.name, 'Box')

# Use the delete method to remove documents
result: DeleteResponse = engine.delete(Model=Product, query=query)
```
///

### Arguments

- `Model: type[DbModel]`: The class that inherits from `DbModel` and serves as the base for querying the database.
- `query: ComparisonOperator | LogicalOperator`: A query that defines the criteria for selecting the documents to be deleted.
- `raw_query: dict (optional)`: A raw query in dictionary format accepted by MongoDB.

!!! warning
    Under the hood, the `delete` method uses MongoDB's `delete_many` operation to remove documents. All documents that match the query criteria will be deleted from the collection.


## Delete one

The `delete_one` method is similar to the `delete` method, with the key difference being that it will delete only the first document that matches the specified query.

/// tab | Async
```python
from pyodmongo import AsyncDbEngine, DeleteResponse

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')
result: DeleteResponse = async engine.delete_one(Model=Product, query=query)
```
///
/// tab | Sync
```python
from pyodmongo import DbEngine, DeleteResponse

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')
result: DeleteResponse = engine.delete_one(Model=Product, query=query)
```
///

## Delete Response
The `DeleteResponse` is the return object for the `delete` and `delete_one` methods, providing information about the result of the delete operation.

### Attributes

- `acknowledged: bool`: Indicates whether the delete operation was acknowledged by the MongoDB server. If `True`, it means the server acknowledged the operation; otherwise, it's `False`.
- `deleted_count: int`: Represents the number of documents that were successfully deleted by the operation. This count may vary depending on the query criteria.
- `raw_result: dict`: A dictionary containing the raw result of the delete operation as returned by the MongoDB driver. It provides additional details about the operation's outcome.