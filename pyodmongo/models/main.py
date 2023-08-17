from datetime import datetime
from .id_model import Id
from ..services.model_init import field_infos
from .db_field_info import DbFieldInfo
from pydantic import BaseModel
from ..pydantic_version import is_pydantic_v1
if not is_pydantic_v1:
    from pydantic import ConfigDict
from pprint import pprint
class MainModel:
    
    __is_pyodmongo_model__ = None
    
    @classmethod
    def __model_fields__(cls):
        fields = {}
        for base_cls in cls.mro():
            base_fields = base_cls.__dict__.get('__annotations__')
            if type(base_fields) == dict:
                fields.update(base_fields)
        return fields
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        print(f'------{cls}------')
        for field_name, field_type in cls.__model_fields__().items():
            field_info: DbFieldInfo = field_infos(field_name=field_name, field_type=field_type, path=[field_name])
            setattr(cls, field_name, field_info)
        print(f'-----------------')
            
class DbModel(MainModel):
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