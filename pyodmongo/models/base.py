from dataclasses import dataclass
from typing import Any


@dataclass
class Base:
    cls: Any = None
    field_name: str = None
    field_type: Any = None
    default_value: Any = None
    base: Any = None
    

