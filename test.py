from pyodmongo.pydantic_mod.main import BaseModel
from datetime import datetime


class DbModel(BaseModel):
    id: str = None
    created_at: datetime = None
    updated_at: datetime = None

    @classmethod
    def __pydantic_init_subclass__(cls):
        for field in cls.model_fields:
            setattr(cls, field, 'VALOR DA VARIAVEL DE CLASSE')
        pass


# class DbModel(Engine):
#     pass


class Model1(DbModel):
    attr1: str = 'ATTR1 VALOR'


class Model2(Model1):
    attr2: str = 'VALOR DO OBJ'


obj_2 = Model2()
print(obj_2)
print(Model2.attr2)
