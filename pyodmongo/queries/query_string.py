from ..models.db_model import DbModel
from ..models.db_field_info import DbField
from ..models.query_operators import LogicalOperator, ComparisonOperator
from .comparison_operators import comparison_operator
from .logical_operators import and_
from typing import Type


def is_inheritance_of_db_model(Model):
    if Model == DbModel:
        return True
    bases = Model.__bases__
    for base in bases:
        if is_inheritance_of_db_model(Model=base):
            return True
    return False


def mount_query_filter(
    Model: Type[DbModel],
    items: dict,
    initial_comparison_operators: list[ComparisonOperator],
) -> LogicalOperator:
    is_inheritance = is_inheritance_of_db_model(Model=Model)
    if not is_inheritance:
        raise TypeError("Model must be a DbModel")
    for key, value in items.items():
        value = value.strip()
        if value == "":
            continue
        split_result = key.strip().rsplit(sep="_", maxsplit=1)
        operator = f"${split_result[-1]}"
        if operator not in ["$eq", "$gt", "$gte", "$in", "$lt", "$lte", "$ne", "$nin"]:
            continue
        try:
            value = eval(value)
        except (SyntaxError, NameError):
            value = value
        field_name = split_result[0]
        try:
            db_field_info: DbField = getattr(Model, field_name)
        except AttributeError:
            raise AttributeError(f"There's no field '{field_name}' in {Model.__name__}")
        initial_comparison_operators.append(
            comparison_operator(field=db_field_info, operator=operator, value=value)
        )
    if len(initial_comparison_operators) == 0:
        return None
    return and_(*initial_comparison_operators)
