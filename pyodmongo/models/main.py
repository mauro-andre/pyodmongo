from datetime import datetime
from .id_model import Id
from ..services.model_init import field_infos, set_new_field_info
from .field_info import FieldInfo
from pydantic import BaseModel
from ..pydantic_version import is_pydantic_v1
if not is_pydantic_v1:
    from pydantic import ConfigDict

class MainModel:
    __is_pyodmongo_model__ = True
    
    @classmethod
    def __model_fields__(cls):
        fields = {}
        for base_cls in reversed(cls.mro()):
            try:
                fields.update(base_cls.__dict__['__annotations__'])
            except KeyError:
                pass
        return fields
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        print(f'------{cls}------')
        for field_name, field_type in cls.__model_fields__().items():
            field_info = field_infos(field_name=field_name, field_type=field_type)
            setattr(cls, field_name, 'VRAU VRAU')
            print()
        print(f'-----------------')
            
class DbModel(BaseModel, MainModel):
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