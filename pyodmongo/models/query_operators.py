from pydantic import BaseModel
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
