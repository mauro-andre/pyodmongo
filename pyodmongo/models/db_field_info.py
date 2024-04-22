from typing import Any
from dataclasses import dataclass


@dataclass
class DbField:
    field_name: str = None
    field_alias: str = None
    path_str: str = None
    field_type: Any = None
    by_reference: bool = None
    is_list: bool = None
    has_model_fields: bool = None
