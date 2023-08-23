from typing import Any, TYPE_CHECKING, Type, TypeVar, ClassVar, Annotated
from pydantic_copy import BaseModel, Field
from datetime import datetime

# class DbModelCore:
#     @classmethod


# class DbCore:
#     @classmethod
#     def __init_subclass__(cls):
#         setattr(cls, 'id', 'VALOR DA VARIAVEL DE CLASSE')


class DbModel(BaseModel):
    id: str = Field(default=None)
    created_at: datetime = None
    updated_at: datetime = None

    # @classmethod
    # def __init_subclass__(cls):
    #     for field in cls.model_fields:
    #         setattr(cls, field, 'VALOR DA VARIAVEL DE CLASSE')

    @classmethod
    def __pydantic_init_subclass__(cls):
        test: type[Annotated] = 'VRAU'
        # setattr(cls, 'id', 'VALOR DA VARIAVEL DE CLASSE')
        for field in cls.model_fields:
            setattr(cls, field, 'VALOR DA VARIAVEL DE CLASSE')
        print()
        pass


# class DbModel(Engine):
#     pass


class Model1(DbModel):
    attr1: str = 'ATTR1 VALOR'


class Model2(Model1):
    attr2: str = 'VALOR DO OBJ'


obj_2 = Model2(attr1='um')
print(obj_2)
print(Model2.attr2)

# class Query:
#     def __getattribute__(self, __name: str) -> Any:
#         print(f'ATRIBUTO: {__name}')


# def eq(Model: type[Model]) -> Model:
#     return Query()


# query = eq(Model2).attr2
