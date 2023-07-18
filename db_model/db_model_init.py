from pydantic import BaseModel
from pymongo import IndexModel, ASCENDING
from .aggregate import lookup_and_set
from typing import get_origin, get_args
from .id_model import Id


def resolve_indexes(key: str, extra: dict):
    idx = []
    is_index = extra.get('index')
    if is_index:
        is_unique = False
        if extra.get('unique'):
            is_unique = True
        idx = [IndexModel([(key, ASCENDING)], name=key, unique=is_unique)]
    return idx


# def resolve_lookup_pipeline(key: str, field_type, is_list: bool, add_field_pipeline: list):
#     lookup = [{
#         '$lookup': {
#             'from': field_type._collection,
#             'localField': key,
#             'foreignField': '_id',
#             'as': key
#         }
#     }]
#     if is_list:
#         return lookup
#     if len(add_field_pipeline) == 0:
#         add_fields = {'$addFields': {
#             key: {'$arrayElemAt': [f'${key}', 0]}}}
#         add_field_pipeline.append(add_fields)
#     else:
#         add_field_pipeline[0]['$addFields'][key] = {
#             '$arrayElemAt': [f'${key}', 0]}
#     return lookup


def resolve_lookup_and_set(cls: BaseModel, pipeline: list, path: str):
    for key in cls.__fields__.keys():
        field_type = get_args(cls.__fields__[key].type_) or cls.__fields__[
            key].type_
        try:
            by_reference = field_type[1] == Id
        except TypeError:
            by_reference = False
        is_list = False
        if by_reference:
            is_list = get_origin(cls.__annotations__[key]) == list
            try:
                field_type = field_type[0]
            except TypeError:
                pass

        has_dict_method = hasattr(field_type, 'dict')

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
