from pydantic import BaseModel
from .db_field_info import DbField
from typing import Any


class ComparisonOperator(BaseModel):
    path_str: str
    operator: str
    value: Any


class _LogicalOperator(BaseModel):
    operator: str
    operators: tuple[ComparisonOperator, ...]


class LogicalOperator(_LogicalOperator):
    operators: tuple[ComparisonOperator | _LogicalOperator, ...]


class SortOperator(BaseModel):
    operators: tuple[tuple[DbField, int], ...]
