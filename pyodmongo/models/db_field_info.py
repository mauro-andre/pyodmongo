from dataclasses import dataclass
from typing import Any
from pydantic import BaseModel, ConfigDict


class DbFieldInfo(BaseModel):
    field_name: str = None
    field_alias: str = None
    path_str: str = None
    field_type: Any = None
    by_reference: bool = None
    is_list: bool = None
    has_model_fields: bool = None
    model_config = ConfigDict(extra='allow')
