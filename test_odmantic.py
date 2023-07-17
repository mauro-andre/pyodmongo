from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from odmantic import AIOEngine
from odmantic import Model, Reference

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB_NAME = 'ODMANTIC_TESTS'

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
client = AsyncIOMotorClient("mongodb://localhost:27017/")
engine = AIOEngine(client=client, database="example_db")


class City(Model):
    name: str
    state: str

    class Config:
        collection = "cities"


class Address(Model):
    street: str
    number: int
    city: City = Reference()

    class Config:
        collection = "addresses"


class User(Model):
    name: str
    phone: int
