from bson import ObjectId
from ..models.id_model import Id
from ..models.db_field_info import DbFieldInfo
from ..models.query_operators import ComparisonOperator
from typing import Any


def comparison_operator(field_info: DbFieldInfo, operator: str, value: Any) -> ComparisonOperator:
    if field_info.by_reference or field_info.field_type == Id:
        if type(value) != list and value is not None:
            value = ObjectId(value)
        if type(value) == list:
            value = [ObjectId(v) for v in value]
    return ComparisonOperator(path_str=field_info.path_str, operator=operator, value=value)


def eq(field_info: DbFieldInfo, value: Any) -> ComparisonOperator:
    return comparison_operator(field_info=field_info, operator='$eq', value=value)


def gt(field_info: DbFieldInfo, value) -> ComparisonOperator:
    return comparison_operator(field_info=field_info, operator='$gt', value=value)


def gte(field_info: DbFieldInfo, value) -> ComparisonOperator:
    return comparison_operator(field_info=field_info, operator='$gte', value=value)


def in_(field_info: DbFieldInfo, value: list) -> ComparisonOperator:
    return comparison_operator(field_info=field_info, operator='$in', value=value)


def lt(field_info: DbFieldInfo, value) -> ComparisonOperator:
    return comparison_operator(field_info=field_info, operator='$lt', value=value)


def lte(field_info: DbFieldInfo, value) -> ComparisonOperator:
    return comparison_operator(field_info=field_info, operator='$lte', value=value)


def ne(field_info: DbFieldInfo, value) -> ComparisonOperator:
    return comparison_operator(field_info=field_info, operator='$ne', value=value)


def nin(field_info: DbFieldInfo, value: list) -> ComparisonOperator:
    return comparison_operator(field_info=field_info, operator='$nin', value=value)


def text(value) -> ComparisonOperator:
    return ComparisonOperator(path_str='$text', operator='$search', value=f'"{value}"')
