from dataclasses import dataclass
from typing import Any


@dataclass
class DbFieldInfo:
    field_name: str = None
    field_alias: str = None
    path: str = None
    field_type: Any = None
    by_reference: bool = None
    is_list: bool = None
    has_model_fields: bool = None
    # default_value: Any = None
