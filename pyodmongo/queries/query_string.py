from ..models.db_model import DbModel
from ..models.db_field_info import DbFieldInfo
from ..models.query_operators import LogicalOperator, ComparisonOperator
from .comparison_operators import comparison_operator
from .logical_operators import and_
from typing import Type


def mount_query_filter(Model: Type[DbModel], items: dict, initial_comparison_operators: list[ComparisonOperator]) -> LogicalOperator:
    if DbModel not in Model.__bases__:
        raise TypeError('Model must be a DbModel')
    for key, value in items.items():
        value = value.strip()
        if value == '':
            continue
        split_result = key.strip().rsplit(sep='_', maxsplit=1)
        operator = f'${split_result[-1]}'
        if operator not in ['$eq', '$gt', '$gte', '$in', '$lt', '$lte', '$ne', '$nin']:
            continue
        try:
            value = eval(value)
        except (SyntaxError, NameError):
            value = value
        field_name = split_result[0]
        try:
            db_field_info: DbFieldInfo = getattr(Model, field_name)
        except AttributeError:
            raise AttributeError(f"There's no field '{field_name}' in {Model.__name__}")
        initial_comparison_operators.append(comparison_operator(field_info=db_field_info, operator=operator, value=value))
    if len(initial_comparison_operators) == 0:
        return {}
    return and_(*initial_comparison_operators)
