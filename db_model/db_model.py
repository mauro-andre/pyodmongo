from .main_model import MainModel
from bson import ObjectId
from datetime import datetime
from pymongo import IndexModel, ASCENDING
from typing import get_origin, get_args
from pprint import pprint


class Id(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(v)
        except Exception as e:
            raise ValueError('invalid ObjectId')

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class DbModel(MainModel):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None
    _pipeline: list = []

    def __init__(self, **attrs):
        if attrs.get('_id') is not None:
            attrs['id'] = attrs.pop('_id')
        super().__init__(**attrs)

    @staticmethod
    def __resolve_indexes(key: str, extra: dict):
        idx = []
        is_index = extra.get('index')
        if is_index:
            is_unique = False
            if extra.get('unique'):
                is_unique = True
            idx = [IndexModel([(key, ASCENDING)], name=key, unique=is_unique)]
        return idx

    @staticmethod
    def __resolve_lookup_pipeline(key: str, field_type, is_list: bool, add_field_pipeline: list):
        lookup = [{
            '$lookup': {
                'from': field_type._collection,
                'localField': key,
                'foreignField': '_id',
                'as': key
            }
        }]
        if is_list:
            return lookup
        if len(add_field_pipeline) == 0:
            add_fields = {'$addFields': {
                key: {'$arrayElemAt': [f'${key}', 0]}}}
            add_field_pipeline.append(add_fields)
        else:
            add_field_pipeline[0]['$addFields'][key] = {
                '$arrayElemAt': [f'${key}', 0]}
        return lookup

    def __init_subclass__(cls):
        indexes = []
        reference_pipeline = []
        add_field_pipeline = []
        for key in cls.__fields__.keys():
            extra = cls.__fields__[key].field_info.extra
            idx = cls.__resolve_indexes(key=key, extra=extra)
            indexes += idx
            field_type = get_args(cls.__fields__[key].type_) or cls.__fields__[
                key].type_
            try:
                by_reference = field_type[1] == Id
            except TypeError:
                by_reference = False

            if by_reference:
                is_list = get_origin(cls.__annotations__[key]) == list
                try:
                    field_type = field_type[0]
                except TypeError:
                    pass
                reference_pipeline += cls.__resolve_lookup_pipeline(key=key,
                                                                    field_type=field_type,
                                                                    is_list=is_list,
                                                                    add_field_pipeline=add_field_pipeline)
        reference_pipeline += add_field_pipeline
        setattr(cls, '_indexes', indexes)
        setattr(cls, '_reference_pipeline', reference_pipeline)

    class Config:
        anystr_strip_whitespace = True
