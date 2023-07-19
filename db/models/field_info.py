from .main_model import MainModel


class FieldInfo(MainModel):
    name: str
    field_type: type
    by_reference: bool
    is_list: bool
    has_dict_method: bool
