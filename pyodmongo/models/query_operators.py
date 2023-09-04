from ..pydantic.main import BaseModel
from typing import Any


class ComparisonOperator(BaseModel):
    path_str: str
    operator: str
    value: Any

    def operator_dict(self):
        return {self.path_str: {self.operator: self.value}}


class LogicalOperator(BaseModel):
    operator: str
    comparison_operators: tuple[ComparisonOperator, ...]

    def operator_dict(self):
        return {self.operator: [lo.operator_dict() for lo in self.comparison_operators]}
