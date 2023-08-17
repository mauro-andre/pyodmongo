from pyodmongo import DbModel, Id, DbField
from bson import ObjectId
from pyodmongo.pydantic_version import is_pydantic_v1
from pydantic import Field
from typing import Union
if not is_pydantic_v1:
    from pydantic import ConfigDict



class MyModel1(DbModel):
    attr1: str#= Field(alias='attr_1_alias')
    attr2: str = 'attr_2'
    
    # if not is_pydantic_v1:
    #     model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
        
    # else:
    #     class Config:
    #         anystr_strip_whitespace = True
    #         validate_assignment = True
            
class MyModel2(MyModel1):
    attr3: str = 'valor padrão'

class MyModel3(DbModel):
    my_model_1: MyModel1 = DbField(index=True, unique=True, text_index=True)
    my_model_1_ref: Id | MyModel1
    my_model_1_union: Union[MyModel1, Id]
    list_my_model_1: list[Id | MyModel1]
    list_my_model_1_union: list[Union[Id, MyModel1]]
    
# obj = MyModel1(id=ObjectId('64dce79ef2af418b2e34482f'), attr1='shunda')
# print(MyModel1.attr2)


# print(MyModel1.model_fields)
# print(obj)
# print(type(obj.id))

# if pydantic.__version__ < "2.0.0":
#     from pydantic import BaseModel
# else:
#     from pydantic.v1 import BaseModel
    
# print(LooseVersion(pydantic.__version__))    

# from pydantic import BaseModel, field_validator, create_model
# # from pydantic.dataclasses import dataclass
# from typing import Union, ClassVar, Mapping, Any
# from dataclasses import dataclass
# from beanie import Document
# import asyncio


# class CoreModel:
    
#     @classmethod
#     def my_model_fields(cls):
#         fields = {}
#         for base_cls in reversed(cls.mro()):
#             try:
#                 fields.update(base_cls.__dict__['__annotations__'])
#             except KeyError:
#                 pass
#         return fields
    
#     @classmethod
#     def __init_subclass__(cls, **kwargs):
#         print(f'-----{cls}-----')
#         print('ESTOU NO GENERIC INIT SUBCLASS')
#         for field_name, field_type in cls.my_model_fields().items():
#             print(field_name, field_type)
#             setattr(cls, field_name, 'VRAU VRAU')
#             pass
#     #     super().__init_subclass__(**kwargs)
#     #     cls.__my_init_subclass__()
#     #     print(f'---------------')
    
#     # @classmethod
#     # def __my_init_subclass__(cls):
#     #     print('AQUIIIIEEEEEE')
        
# class MyPModel(BaseModel):
#     @classmethod
#     def __pydantic_init_subclass__(cls):
#         print(f'-----{cls}-----')
#         for field_name in cls.model_fields.keys():
#             setattr(cls, field_name, 'VRAUUEEE')
#             pass
#         print(f'---------------')

# MergedModel = create_model('MergedModel')

# class MainModel(CoreModel):
#     attr_main: str = None
    
#     @classmethod
#     def __init_subclass__(cls, **kwargs):
#         print(f'-----{cls}-----')
#         print('ESTOU NO GENERIC INIT SUBCLASS')
#         for field_name, field_type in cls.my_model_fields().items():
#             print(field_name, field_type)
#             setattr(cls, field_name, 'VRAU VRAU')


# class One(MainModel):
#     attr_1: str = None
#     attr_11: str = None
    
# class Two(One):
#     attr_2: Union[str, int] = None
#     attr_22: str = None
    
    
# class Three(Two):
#     attr_3: str = None


# print(Three.attr_1)
    
    
