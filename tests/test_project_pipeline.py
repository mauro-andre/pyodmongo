from pyodmongo import DbModel, Field, AsyncDbEngine
from pydantic import ConfigDict
from typing import ClassVar
import pytest_asyncio
import pytest


def to_lower_camel(string: str) -> str:
    words = string.split("_")
    return "".join(words[:1] + [word.capitalize() for word in words[1:]])


mongo_uri = "mongodb://localhost:27017"
db_name = "pyodmongo_pytest"
engine = AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name)


class MyModel(DbModel):
    name: str
    age: int
    one_name: str
    other_name: str
    _collection: ClassVar = "my_model"
    # model_config = ConfigDict(alias_generator=to_lower_camel)


class MyModelRead(DbModel):
    name: str
    other_name: str
    _collection: ClassVar = "my_model"


@pytest_asyncio.fixture()
async def drop_collections():
    await engine._db[MyModel._collection].drop()
    yield
    await engine._db[MyModel._collection].drop()


@pytest.mark.asyncio
async def test_project_pipilene(drop_collections):
    obj_my_model = MyModel(
        name="A name", age=10, one_name="One Name", other_name="Other Name"
    )
    await engine.save(obj_my_model)
    obj_my_model_read = await engine.find_one(Model=MyModelRead)
    assert obj_my_model_read.name == "A name"
    assert obj_my_model_read.other_name == "Other Name"
