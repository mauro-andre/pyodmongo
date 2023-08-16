from pydantic import BaseModel, field_validator, create_model
# from pydantic.dataclasses import dataclass
from typing import Union, ClassVar, Mapping, Any
from dataclasses import dataclass
from beanie import Document
import asyncio


class CoreModel:
    
    @classmethod
    def my_model_fields(cls):
        fields = {}
        for base_cls in reversed(cls.mro()):
            try:
                fields.update(base_cls.__dict__['__annotations__'])
            except KeyError:
                pass
        return fields
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        print(f'-----{cls}-----')
        print('ESTOU NO GENERIC INIT SUBCLASS')
        for field_name, field_type in cls.my_model_fields().items():
            print(field_name, field_type)
            setattr(cls, field_name, 'VRAU VRAU')
            pass
    #     super().__init_subclass__(**kwargs)
    #     cls.__my_init_subclass__()
    #     print(f'---------------')
    
    # @classmethod
    # def __my_init_subclass__(cls):
    #     print('AQUIIIIEEEEEE')
        
class MyPModel(BaseModel):
    @classmethod
    def __pydantic_init_subclass__(cls):
        print(f'-----{cls}-----')
        for field_name in cls.model_fields.keys():
            setattr(cls, field_name, 'VRAUUEEE')
            pass
        print(f'---------------')

MergedModel = create_model('MergedModel')

class MainModel(CoreModel):
    attr_main: str = None
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        print(f'-----{cls}-----')
        print('ESTOU NO GENERIC INIT SUBCLASS')
        for field_name, field_type in cls.my_model_fields().items():
            print(field_name, field_type)
            setattr(cls, field_name, 'VRAU VRAU')


class One(MainModel):
    attr_1: str = None
    attr_11: str = None
    
class Two(One):
    attr_2: Union[str, int] = None
    attr_22: str = None
    
    
class Three(Two):
    attr_3: str = None


print(Three.attr_1)
    
    
