from pydantic import BaseModel
from .db_field_info import DbField


class SortOperator(BaseModel):
    operators: tuple[tuple[DbField, int], ...]
