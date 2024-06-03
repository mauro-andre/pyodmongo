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
