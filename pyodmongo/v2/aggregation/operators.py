from ..models.db_field import DbField
from typing import Any


def eq(field: DbField, value: Any):
    return field.__eq__(value)


def ne(field: DbField, value: Any):
    return field.__ne__(value)


def lt(field: DbField, value: Any):
    return field.__lt__(value)


def lte(field: DbField, value: Any):
    return field.__le__(value)


def gt(field: DbField, value: Any):
    return field.__gt__(value)


def gte(field: DbField, value: Any):
    return field.__ge__(value)


def in_(field: DbField, values: list) -> dict:
    return {"$in": [field.path_str, values]}


def nin(field: DbField, values: list) -> dict:
    return {"$nin": [field.path_str, values]}


def and_(*expressions: dict) -> dict:
    return {"$and": list(expressions)}


def or_(*expressions: dict) -> dict:
    return {"$or": list(expressions)}


def nor(*expressions: dict) -> dict:
    return {"$nor": list(expressions)}


def not_(expression: dict) -> dict:
    return {"$not": [expression]}
