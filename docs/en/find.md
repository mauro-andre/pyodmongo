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
- `sort: SortOperator`: An optional parameter that specifies the sort order of the results. Each tuple in the list contains a field name and a direction (`1` for ascending, `-1` for descending). This parameter allows for sorting the results based on one or more fields, helping in organizing the retrieved data as per specific requirements.
- `raw_sort: dict`: An optional parameter similar to `sort` but uses a dictionary format directly compatible with MongoDB sort specifications. It's particularly useful when complex sorting criteria are needed that are directly supported by MongoDB. This can provide more direct control over the sorting process in the database query.
- `populate: bool`: A boolean flag that determines whether the returned object will have its relationship fields populated with other objects or will only contain the `id` field.
- `as_dict: bool`:  A boolean flag that, when set to `True`, returns the response as a dictionary instead of instantiated objects. This is particularly useful when a lightweight, serializable format is required, such as for JSON responses in web applications, or when the consumer prefers to work with basic data structures rather than complex object models.
- `tz_info: timezone`: An optional parameter that specifies the time zone information for any `datetime` fields in the retrieved objects. This parameter is crucial when dealing with records in different time zones and ensures that the `datetime` values are correctly adjusted to the specified time zone. If not set, the `datetime` fields will be returned in the default time zone of the database or the application server.

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

- When you enable `populate=True` in `find_one` o `find_many`, **PyODMongo** will populate all references within that object.
- If the references themselves have additional references, **PyODMongo** will recursively populate those as well, traversing through all levels of reference.
- Reference lists are also populated.

!!! note
    To ensure excellent performance, **PyODMongo** leverages the power of MongoDB's Aggregation framework under the hood. The Aggregation framework is a powerful and efficient tool for processing and transforming data within MongoDB. 

