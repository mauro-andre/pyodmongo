from dataclasses import dataclass


@dataclass
class DbFieldInfo:
    field_name: str = None
    field_type: type = None
    by_reference: bool = None
    is_list: bool = None
    is_pyodmongo_model: bool = None
    

