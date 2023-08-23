from datetime import datetime
from typing import Any
from .id_model import Id
from .base import Base
from pyodmongo import BaseModel
from ..pydantic_version import is_pydantic_v1
if not is_pydantic_v1:
    from pyodmongo import ConfigDict
    from pyodmongo._internal._model_construction import ModelMetaclass
else:
    from pyodmongo.main import ModelMetaclass
from pprint import pprint
from dataclasses import dataclass

# class DbModelMeta(ABCMeta):
#     def __init__(cls, name, bases, namespace):
#         super().__init__(name, bases, namespace)
        
#         init_code = []
#         for attr_name, attr_value in cls.__annotations__.items():
#             init_code.append(f"self.{attr_name} = {attr_name}")
        
#         init_code = "\n    ".join(init_code)
        
#         exec(f"def __init__(self, {', '.join(cls.__annotations__)}) -> None:\n    {init_code}", globals(), locals())
#         setattr(cls, '__init__', locals()['__init__'])
        
#         cls.__signature__ = cls.__init__.__signature__
class MainModel:
    pass
    __is_pyodmongo_model__ = None
    
    @classmethod
    def __model_fields__(cls):
        bases = []
        for base_cls in cls.mro():
            base_fields = base_cls.__dict__.get('__annotations__')
            # pprint(base_cls.__dict__)
            if type(base_fields) == dict:
                for key, value in base_fields.items():
                    default_value = base_cls.__dict__.get(key)
                    # print(f'key: {key}, base: {base_cls}, default_value: {default_value}')
                    base = Base(cls=cls, field_name=key, field_type=value, default_value=default_value, base=base_cls)
                    # setattr(base.cls, base.field_name, 'AAAAAAA')
                    # print(base)
                    bases.append(base)
                    # print(f'base_cls: {base_cls}')
                    # print(f'base: {base}')
        return bases
    
    @classmethod
    def __init_subclass__(cls):
        print(f'------{cls}------')
        bases = cls.mro()
        for field in cls.model_fields:
            print(field)
            # setattr(cls, field, 'VRAU')
        # bases = cls.__model_fields__()
        # for base in bases:
        #     base: Base
        #     vrau: str = 'VRAU DO TIPO STR'
            # setattr(base.cls, base.field_name, vrau)
            # field_info: DbFieldInfo = field_infos(base=base, path=[base.field_name])
            # print(field_info)
            # print(base)
            # setattr(cls, 'id', 'AAAAAAAAAAAAAA')
        # for field_name, field_type in cls.__model_fields__().items():
        #     field_info: DbFieldInfo = field_infos(cls=cls, field_name=field_name, field_type=field_type, path=[field_name])
        # print(f'-----------------')
        # pass


def modificator(cls: BaseModel):
    def wrapper(cls: BaseModel):
        print(cls.mro())
        return cls
    return wrapper(cls)

class DbModel(BaseModel):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None
    
    @classmethod
    def __pydantic_init_subclass__(cls):
        print(f'------{cls}------')
        for field in cls.model_fields:
            # print(field)
            setattr(cls, field, 'VRAU VREU')
        print(f'-----------------')


    # if not is_pydantic_v1:+
    #     model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, populate_by_name=True)
        
    # else:
    #     class Config:
    #         anystr_strip_whitespace = True
    #         validate_assignment = True
    #         allow_population_by_field_name = True
    
    # @classmethod
    # def __pydantic_init_subclass__(cls):
    #     print('TO NO PYDANTIC INIT')
        
