from pydantic import BaseModel, ConfigDict

class FieldInfo(BaseModel):
    field_name: str = None
    field_type: type = None
    by_reference: bool = None
    is_list: bool = None
    has_model_dump: bool = None
    model_config = ConfigDict(extra='allow', str_strip_whitespace=True)

