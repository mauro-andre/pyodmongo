from bson import ObjectId
from ..models.id_model import Id
from ..models.db_field_info import DbField
from ..models.query_operators import ComparisonOperator
from typing import Any


def comparison_operator(
    field: DbField, operator: str, value: Any
) -> ComparisonOperator:
    if field.by_reference or field.field_type == Id:
        if type(value) != list and value is not None:
            value = ObjectId(value)
        if type(value) == list:
            value = [ObjectId(v) for v in value]
    return ComparisonOperator(path_str=field.path_str, operator=operator, value=value)


def eq(field: DbField, value: Any) -> ComparisonOperator:
    return comparison_operator(field=field, operator="$eq", value=value)


def gt(field: DbField, value) -> ComparisonOperator:
    return comparison_operator(field=field, operator="$gt", value=value)


def gte(field: DbField, value) -> ComparisonOperator:
    return comparison_operator(field=field, operator="$gte", value=value)


def in_(field: DbField, value: list) -> ComparisonOperator:
    return comparison_operator(field=field, operator="$in", value=value)


def lt(field: DbField, value) -> ComparisonOperator:
    return comparison_operator(field=field, operator="$lt", value=value)


def lte(field: DbField, value) -> ComparisonOperator:
    return comparison_operator(field=field, operator="$lte", value=value)


def ne(field: DbField, value) -> ComparisonOperator:
    return comparison_operator(field=field, operator="$ne", value=value)


def nin(field: DbField, value: list) -> ComparisonOperator:
    return comparison_operator(field=field, operator="$nin", value=value)


def text(value) -> ComparisonOperator:
    return ComparisonOperator(path_str="$text", operator="$search", value=f'"{value}"')
