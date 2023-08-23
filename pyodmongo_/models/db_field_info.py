from dataclasses import dataclass
from typing import Any


@dataclass
class DbFieldInfo:
    field_name: str = None
    field_type: Any = None
    by_reference: bool = None
    is_list: bool = None
    is_pyodmongo_model: bool = None
    default_value: Any = None
    

