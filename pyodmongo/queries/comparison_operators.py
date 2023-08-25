from bson import ObjectId
from ..models.id_model import Id
from ..models.db_field_info import DbFieldInfo


def comparison_operator(field_info: DbFieldInfo, operator, value):
    if field_info.by_reference or field_info.field_type == Id:
        if type(value) != list and value is not None:
            value = ObjectId(value)
        if type(value) == list:
            value = [ObjectId(v) for v in value]
    return {field_info.path_str: {operator: value}}


def eq(field_info: DbFieldInfo, v):
    return comparison_operator(field_info=field_info, operator='$eq', value=v)


def gt(field_info, v):
    return comparison_operator(field_info=field_info, operator='$gt', value=v)


def gte(field_info, v):
    return comparison_operator(field_info=field_info, operator='$gte', value=v)


def in_(field_info, v: list):
    return comparison_operator(field_info=field_info, operator='$in', value=v)


def lt(field_info, v):
    return comparison_operator(field_info=field_info, operator='$lt', value=v)


def lte(field_info, v):
    return comparison_operator(field_info=field_info, operator='$lte', value=v)


def ne(field_info, v):
    return comparison_operator(field_info=field_info, operator='$ne', value=v)


def nin(field_info, v: list):
    return comparison_operator(field_info=field_info, operator='$nin', value=v)


def text(v):
    return {'$text': {'$search': f'"{v}"'}}
