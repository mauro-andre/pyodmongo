from .main_model import MainModel


class FieldInfo(MainModel):
    name: str = None
    field_type: type = None
    by_reference: bool = None
    is_list: bool = None
    has_dict_method: bool = None

    class Config:
        extra = 'allow'
