# <center>Use with FastAPI</center>

**PyODMongo** is fully compatible with FastAPI due to its Pydantic foundation. This compatibility allows you to use **PyODMongo** in FastAPI applications in an elegant and efficient way, allowing the creation of dynamic queries at runtime.

```python
from fastapi import FastAPI, Request
from pyodmongo import DbModel, AsyncDbEngine
from pyodmongo.queries import mount_query_filter
from typing import ClassVar

app = FastAPI()
engine = AsyncDbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class MyModel(DbModel):
    attr1: str
    attr2: str
    attr3: int
    _collection: ClassVar = "my_model"


@app.get("/", response_model=list[MyModel])
async def get_route(request: Request):
    query, sort = mount_query_filter(
        Model=MyModel,
        items=request.query_params._dict,
        initial_comparison_operators=[],
    )
    return await engine.find_many(Model=MyModel, query=query, sort=sort)
```

In the example above, we defined a FastAPI route `GET /` that accepts query parameters. The `mount_query_filter` function, designed for use with FastAPI `Request`, dynamically constructs a query based on the items in these parameters.

## The `mount_query_filter` Function

The `mount_query_filter` function adapts perfectly to FastAPI. It dynamically builds a query based on the passed dictionary items, making it compatible with the `request.query_params._dict` attribute, which contains the route's query strings.

### Function Parameters

- `Model: type[DbModel]`: The model for which the query will be constructed.
- `items: dict`: A dictionary containing items to construct the query.
- `initial_comparison_operators: list[ComparisonOperator]`: An initial list of comparison operators to start the query.

The function returns a query with the `and` operator applied between all items in the passed dictionary.

## Example Usage

![Image title](./assets/images/insomnia_request.png)

When you trigger the following route with query strings: `http://localhost:8000/?attr1_eq=value_1&attr2_in=%5B'value_2',%20'value_3'%5D&attr3_gte=10&_sort=%5B%5B'attr1',%201%5D,%20%5B'attr2',%20-1%5D%5D`, the `request.query_params._dict` will contain the following dictionary:

```python
{
    "attr1_eq": "value_1", 
    "attr2_in": "['value_2', 'value_3']", 
    "attr3_gte": 10,
    "_sort": "[['attr1', 1], ['attr2', -1]]",
}
```

In this dictionary, keys must be attribute names followed by an underscore and a valid operator (e.g. 'attr1' + '_' + 'eq'). Valid operators are: `"eq", "gt", "gte", "in", "lt", "lte", "ne", "nin"`.

By using the `mount_query_filter` function in combination with FastAPI's `Request`, you can enable powerful and dynamic query capabilities in your applications.