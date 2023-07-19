from pydantic import BaseModel
from pymongo import IndexModel, ASCENDING
from .aggregate_stages import lookup_and_set
from typing import get_origin, get_args
from ..models.id_model import Id


def field_infos(cls: BaseModel, field_name: str):
    field_type = get_args(cls.__fields__[field_name].type_) or cls.__fields__[
        field_name].type_
    try:
        by_reference = field_type[1] == Id
    except TypeError:
        by_reference = False
    try:
        field_type = field_type[0]
    except TypeError:
        pass
    try:
        is_list = get_origin(cls.__annotations__[field_name]) == list
    except KeyError:
        is_list = False
    has_dict_method = hasattr(field_type, 'dict')
    return field_type, by_reference, is_list, has_dict_method


def resolve_indexes(key: str, extra: dict):
    idx = []
    is_index = extra.get('index')
    if is_index:
        is_unique = False
        if extra.get('unique'):
            is_unique = True
        idx = [IndexModel([(key, ASCENDING)], name=key, unique=is_unique)]
    return idx


def resolve_lookup_and_set(cls: BaseModel, pipeline: list, path: str):
    for key in cls.__fields__.keys():
        field_type, by_reference, is_list, has_dict_method = field_infos(
            cls=cls, field_name=key)

        if has_dict_method:
            if path == '':
                path += key
            else:
                path += f'.{key}'
            if by_reference:
                collection = field_type._collection
                pipeline += lookup_and_set(from_=collection,
                                           local_field=path,
                                           foreign_field='_id',
                                           as_=path,
                                           is_reference_list=is_list)
            if not is_list:
                resolve_lookup_and_set(
                    cls=field_type, pipeline=pipeline, path=path)

    return pipeline
