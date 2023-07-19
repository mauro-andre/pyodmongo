from fastapi import HTTPException
from bson import ObjectId
from ..models.field_info import FieldInfo
from ..models.id_model import Id


def comparison_operator(field_info: FieldInfo, operator, value):
    field_name = field_info.name
    field_type = field_info.field_type
    if field_name == 'id':
        field_name = '_id'
    if field_type == Id:
        if type(value) != list:
            try:
                value = ObjectId(value)
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        if type(value) == list:
            try:
                value = [ObjectId(v) for v in value]
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
    return {field_name: {operator: value}}


def eq(field_info: FieldInfo, v):
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
