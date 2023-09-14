# <center>Find</center>

## Find one

The `find_one` method is available in both `AsyncDbEngine` and `DbEngine` classes of the **PyODMongo** library. This method is used to retrieve a single object from the database based on specified criteria.

/// tab | Async
```python hl_lines="21"
from pyodmongo import AsyncDbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar
import asyncio

# Initialize the database engine
engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

# Define a model class
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

async def main():
    # Define a query (in this case, we're using the 'eq' method from 'pyodmongo.queries')
    query = eq(Product.name, 'Box')

    # Use 'find_one' to retrieve a single product based on the query
    result: Product = await engine.find_one(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="19"
from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar

# Initialize the database engine
engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

# Define a model class
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

# Define a query (in this case, we're using the 'eq' method from 'pyodmongo.queries')
query = eq(Product.name, 'Box')

# Use 'find_one' to retrieve a single product based on the query
result: Product = engine.find_one(Model=Product, query=query)
```
///

### Arguments

- `Model: type[DbModel]`: The class that inherits from `DbModel` to be used for forming the retrieved object from the database.
- `query: ComparisonOperator | LogicalOperator`: The query used to filter the objects in the database.
- `raw_query: dict`: An optional query in the dictionary format compatible with MongoDB.
- `populate: bool`: A boolean flag that determines whether the returned object will have its relationship fields populated with other objects or will only contain the `id` field.

!!! warning
    If `raw_query` is passed, `query` will not be considered.

## Find many

The `find_many` method in the **PyODMongo** library is similar to the `find_one` method, but it retrieves a list of objects that match the specified criteria.

/// tab | Async
```python hl_lines="13"
# Define a model class
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

async def main():
    # Define a query (in this case, we're using the 'eq' method from 'pyodmongo.queries')
    query = gte(Product.price, 5)

    #  Use 'find_many' to retrieve a list of products based on the query
    result: list[Product] = await engine.find_many(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="12"
# Define a model class
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

# Define a query (in this case, we're using the 'gte' method from 'pyodmongo.queries')
query = gte(Product.price, 5)

# Use 'find_many' to retrieve a list of products based on the query
result: list[Product] = engine.find_many(Model=Product, query=query)
```
///

### Arguments

Additionally, it includes three extra arguments for pagination control:

- `Model: type[DbModel]`: The class that inherits from DbModel to be used for forming the retrieved object from the database.
- `query: ComparisonOperator | LogicalOperator`: The query used to filter the objects in the database.
- `raw_query: dict`: An optional query in the dictionary format compatible with MongoDB.
- `populate: bool`: A boolean flag that determines whether the returned object will have its relationship fields populated with other objects or will only contain the id field.
- `paginate: bool`: A boolean flag that specifies whether the response should be paginated or a regular list.
- `current_page: int`: If `paginate=True`, this argument determines the page of results to be retrieved.
- `docs_per_page: int`: If `paginate=True`, this argument determines the maximum number of objects per page in the query results.

### Paginate

When you set `paginate=True` in the `find_many` method of **PyODMongo**, the result of the query will be encapsulated in an object of type `ResponsePaginate`. This allows for efficient and organized retrieval of query results across multiple pages. The `ResponsePaginate` object contains the following attributes:

- `current_page: int`: Indicates the current page of the search results.
- `page_quantity: int`: Represents the total number of pages in the search results.
- `docs_quantity: int`: Specifies the total count of objects found in the search.
- `docs: list[Any]`: Contains the list of objects retrieved for the current page.

This pagination mechanism is particularly useful when dealing with large datasets, as it allows you to break down the results into manageable chunks and navigate through them with ease.

/// tab | Async
```python hl_lines="9"
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

async def main():
    query = gte(Product.price, 5)
    result: ResponsePaginate = await engine.find_many(Model=Product, query=query, paginate=True)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="9"
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


query = gte(Product.price, 5)
result: ResponsePaginate = engine.find_many(Model=Product, query=query, paginate=True)
```
///

## Populate

The populate feature in the **PyODMongo** library is a powerful mechanism for automatically populating all references within an object, including nested references. This feature simplifies working with related data in MongoDB and allows you to access linked documents without having to manually retrieve them one by one. The populate functionality has the following behavior:

- When you enable `populate=True` in `find_one` o `find_many `, **PyODMongo** will populate all references within that object.
- If the references themselves have additional references, **PyODMongo** will recursively populate those as well, traversing through all levels of reference until it encounters a reference that is a list.
- Reference lists are also populated, but if the objects within the list have their own references, they will not be populated.

!!! note
    To ensure excellent performance, **PyODMongo** leverages the power of MongoDB's Aggregation framework under the hood. The Aggregation framework is a powerful and efficient tool for processing and transforming data within MongoDB. 

