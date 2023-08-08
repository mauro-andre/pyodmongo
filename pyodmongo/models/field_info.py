from pydantic import BaseModel

class FieldInfo(BaseModel):
    field_name: str = None
    field_type: type = None
    by_reference: bool = None
    is_list: bool = None
    has_dict_method: bool = None

    class Config:
        extra = 'allow'
        anystr_strip_whitespace = True
