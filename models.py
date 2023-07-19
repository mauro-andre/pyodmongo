from db import DbModel, MainModel
from pydantic import Field
from typing import ClassVar


# class Vrau(DbModel):
#     var1: str
#     var2: str
#     _collection: ClassVar = 'vraus'


# class State(DbModel):
#     name: str
#     sigla: str
#     vraus: list[Vrau] = Field(by_reference=True)
#     _collection: ClassVar = 'states'


# class BrazilianCity(DbModel):
#     name: str = Field(index=True)
#     states: list[State]
#     _collection: ClassVar = 'brazilian_cities'


# class Address(MainModel):
#     street: str
#     city: BrazilianCity
#     number: str


# class Integrator(DbModel):
#     name: str = Field(index=True)
#     address: Address
#     outros_addresses: list[Address]
#     outras_cidades: list[BrazilianCity] = Field(by_reference=True)
#     _collection: ClassVar = 'integrators'
