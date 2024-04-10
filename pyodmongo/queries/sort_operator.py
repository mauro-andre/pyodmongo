from ..models.db_field_info import DbField
from ..models.query_operators import SortOperator


def sort(*operators: tuple[DbField, int]) -> SortOperator:
    return SortOperator(operators=operators)
