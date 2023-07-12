from db_model import MainModel, DbModel
from typing import ClassVar
import asyncio
from pydantic import Field
from bson import ObjectId
from pprint import pprint
from db_model import save, find_one
from fastapi import FastAPI

app = FastAPI()


class Address(MainModel):
    street: str
    number: str


class Integrator(DbModel):
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    address: Address
    _collection: ClassVar = 'integrators'


class User(DbModel):
    username: str = Field(index=True)
    phone_number: str
    integrator: Integrator = Field(by_reference=True)
    _collection: ClassVar = 'users'


address = Address(street='Rua dos bobos', number='123')
integrator = Integrator(id=ObjectId('64add18355e21f9d756d95c8'), name='Integrador Legal 2',
                        email='shunda1@email.com', address=address)
user = User(username='Shunda', phone_number='99999', integrator=integrator)


@app.get('/test')
async def test():
    query = {'_id': ObjectId('64add20cebc30e84159695ee')}
    return await find_one(Model=User, query=query)


# class Test(BaseModel):
#     id: str
#     name: str


# obj_dict = {'_id': 'a1b2c3', 'name': 'Shunda'}
# obj = Test(**obj_dict)
# obj_to_dict = obj.dict()
