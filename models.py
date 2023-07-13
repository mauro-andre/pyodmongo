from db_model import DbModel, MainModel
from pydantic import Field
from typing import ClassVar, List


class BrazilianCity(DbModel):
    name: str = Field(index=True)
    state: str
    _collection: ClassVar = 'brazilian_cities'


class Address(MainModel):
    street: str
    city: BrazilianCity = Field(by_reference=False)
    number: str

# User = ForwardRef('User')


class Integrator(DbModel):
    address: Address
    name: str = Field(index=True)
    outros_addresses: list[Address] = Field(by_reference=False)
    _collection: ClassVar = 'integrators'
