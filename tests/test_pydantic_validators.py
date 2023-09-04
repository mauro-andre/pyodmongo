from pyodmongo import DbModel, Id
from pyodmongo.models.db_model_2 import DbModel2
from pydantic import BaseModel, field_validator, model_validator, ConfigDict, create_model
from typing import ClassVar, TypeVar, Type
from pydantic import BaseModel
from datetime import datetime


# def DbModelDecorator(cls):
#     def wrapper(cls):
#         DbModelDynamic = create_model(
#             'DbModelDynamic',
#             id=(Id, None),
#             created_at=(datetime, None),
#             updated_at=(datetime, None),
#             __base__=cls,
#         )
#         for field in DbModelDynamic.model_fields:
#             setattr(DbModelDynamic, field, 'CLASS VALUE SET')
#         return DbModelDynamic
#     return wrapper(cls=cls)

def DbModelDecorator(cls):
    DbModelDynamic = create_model(
        'DbModelDynamic',
        id=(Id, None),
        created_at=(datetime, None),
        updated_at=(datetime, None),
        __base__=cls,
    )
    for field in DbModelDynamic.model_fields:
        setattr(DbModelDynamic, field, 'CLASS VALUE SET')
    return DbModelDynamic


def test_field_validator():
    @DbModelDecorator
    class MyModel1(BaseModel):
        attr1: str
        attr2: str
        # model_config = ConfigDict()
        # _collection: ClassVar = 'Vrau'

        # @field_validator('attr2')
        # def validate_attr2(cls, value):
        #     return value

    class MyModel2(MyModel1):
        attr3: str
        attr4: str

    obj = MyModel1(attr1='Vrau', attr2='Vrou')
    obj2 = MyModel2(attr1='Vrau', attr2='Vrou', attr3='Vreu', attr4='Vruu')
    print(obj)
    print(obj2)
    # print(MyModel1.id)
    # print(MyModel2.id)
