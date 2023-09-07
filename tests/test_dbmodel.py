from fastapi import FastAPI
from fastapi.testclient import TestClient
from pyodmongo.models.id_model import Id
from datetime import datetime
from pprint import pprint
from typing import Literal, TypeVar, Any
from enum import Enum
from pyodmongo.models.main import DbModel
from bson import ObjectId
from pydantic import Field


app = FastAPI()


class MyClass1(DbModel):
    attr1: str = None
    attr2: str


class MyClass2(MyClass1):
    attr3: str
    attr4: str = None


# class MyClass3(MyClass1, MyClass2):
#     attr5: str
#     attr6: str


# class MyClass4(MyClass3):
#     attr7: str


@app.post('/', response_model=MyClass2)
async def root(model: MyClass2):
    return model

client = TestClient(app)


def test_root():
    json_body = {
        # 'id': str(ObjectId()),
        # 'created_at': datetime(2023, 10, 10, 10, 10, 10),
        # 'updated_at': datetime(2023, 10, 10, 10, 10, 10),
        'attr2': 'vrau',
        'attr3': 'vreu'
    }
    # pprint(MyClass1.__dict__)
    obj = MyClass2(attr2='Vreu', attr3='Vriu')
    print(obj)
    response = client.post('/', json=json_body)
    pprint(response.json())
    ...
