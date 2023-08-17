from abc import ABCMeta
from datetime import datetime
from typing import Any, Annotated, ClassVar
from .id_model import Id
from .base import Base
from ..services.model_init import field_infos
from .db_field_info import DbFieldInfo
from pydantic import BaseModel
from ..pydantic_version import is_pydantic_v1
if not is_pydantic_v1:
    from pydantic import ConfigDict
    from pydantic._internal._model_construction import ModelMetaclass
else:
    from pydantic.main import ModelMetaclass
from pprint import pprint


class MainModelMetaClass(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        print(f'------{name}------')
        pprint(namespace)
        namespace['id'] = 'VRAU VRAU'
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        # setattr(cls, 'id', 'ID_VRAU')
        # print(cls)
        print(f'-----------------')
        return cls

class DbModelMetaClass(MainModelMetaClass, type(BaseModel)):
    pass


class DbModel(BaseModel, metaclass=DbModelMetaClass):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None
    
    if not is_pydantic_v1:
        model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, populate_by_name=True)
        
    else:
        class Config:
            anystr_strip_whitespace = True
            validate_assignment = True
            allow_population_by_field_name = True
    
    @classmethod
    def __pydantic_init_subclass__(cls):
        print('TO NO PYDANTIC INIT')
        
        
        
# class MainModel(metaclass=MainModelMetaClass):
#     pass
    # __is_pyodmongo_model__ = None
    
    # @classmethod
    # def __model_fields__(cls):
    #     bases = []
    #     for base_cls in cls.mro():
    #         base_fields = base_cls.__dict__.get('__annotations__')
    #         pprint(base_cls.__dict__)
    #         if type(base_fields) == dict:
    #             for key, value in base_fields.items():
    #                 default_value = base_cls.__dict__.get(key)
    #                 # print(f'key: {key}, base: {base_cls}, default_value: {default_value}')
    #                 base = Base(cls=cls, field_name=key, field_type=value, default_value=default_value, base=base_cls)
    #                 bases.append(base)
    #                 # print(f'base_cls: {base_cls}')
    #                 # print(f'base: {base}')
    #                 print()
    #     return bases
    
    # @classmethod
    # def __init_subclass__(cls):
    #     print(f'------{cls}------')
    #     bases = cls.__model_fields__()
    #     for base in bases:
    #         base: Base
    #         # field_info: DbFieldInfo = field_infos(base=base, path=[base.field_name])
    #         # print(field_info)
    #         # setattr(cls, base.field_name, field_info)
    #     # for field_name, field_type in cls.__model_fields__().items():
    #     #     field_info: DbFieldInfo = field_infos(cls=cls, field_name=field_name, field_type=field_type, path=[field_name])
    #     #     pass
    #     print(f'-----------------')