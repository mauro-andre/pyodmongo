from ..models.db_model import DbModel
from ..models.db_field_info import DbField
from ..models.query_operators import LogicalOperator, ComparisonOperator
from .comparison_operators import comparison_operator
from .logical_operators import and_
from typing import Type
import re


def is_inheritance_of_db_model(Model):
    if Model == DbModel:
        return True
    bases = Model.__bases__
    for base in bases:
        if is_inheritance_of_db_model(Model=base):
            return True
    return False


def js_regex_to_python(js_regex_str):
    try:
        match = re.match(r"/([^/]+)/([a-z]*)$", js_regex_str)
    except TypeError:
        return js_regex_str
    try:
        pattern, js_flags = match.groups()
    except AttributeError:
        return js_regex_str
    flags = 0
    if "i" in js_flags:
        flags |= re.IGNORECASE
    if "m" in js_flags:
        flags |= re.MULTILINE
    if "s" in js_flags:
        flags |= re.DOTALL

    return re.compile(pattern, flags)


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
        if type(value) is list:
            for index, item in enumerate(value):
                value[index] = js_regex_to_python(item)
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
