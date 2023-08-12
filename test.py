from pydantic import BaseModel, Field
from typing import ClassVar



class MainModel(BaseModel):
    attr_main: str
    
    @classmethod
    def __pydantic_init_subclass__(cls):
        for key in cls.model_fields.keys():
            print(key)
            setattr(cls, key, 'NEW VALUE')
            

class One(MainModel):
    attr_one: str
    test_class_var: ClassVar
    
    
    
class Two(One):
    attr_two: str
    
# setattr(MainModel, 'attr_one', 'VALOR LEGAL')
# setattr(One, 'attr_one', 'VALOR LEGAL')
# setattr(Two, 'attr_one', 'VALOR LEGAL')
# print(Two.attr_main)
# print(Two.attr_main)