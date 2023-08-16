from pydantic import BaseModel
from pymongo import IndexModel, ASCENDING, TEXT
from .aggregate_stages import lookup_and_set
from typing import get_origin, get_args
from ..models.field_info import FieldInfo
from ..models.id_model import Id
from typing import Union, Any
from types import UnionType


def field_infos(field_name: str, field_type: Any):
    print('Estou aqui')
    print(field_name, field_type)
    # info = cls.model_fields[field_name].annotation
    by_reference = False
    is_list = False
    info = get_origin(field_type)
    if info is UnionType or info is Union:
        by_reference = Id in field_type.__args__
        field_type_index = 0
        if by_reference:
            id_index = field_type.__args__.index(Id)
            field_type_index = abs(id_index - 1)
        field_type = field_type.__args__[field_type_index]
    print(f'by_reference: {by_reference}, field_type: {field_type}')
    # if get_origin(info) is Union:
    #     field_type = get_args(info)[0]
    #     by_reference = '_id' in get_args(get_args(info)[1])
    # elif get_origin(info) is list:
    #     field_type = get_args(info)[0]
    #     by_reference = False
    #     is_list = True
    #     info = field_type
    #     if get_origin(info) is Union:
    #         field_type = get_args(field_type)[0]
    #         by_reference = '_id' in get_args(get_args(info)[1])
    # else:
    #     field_type = info
    #     by_reference = False
    # has_model_dump = hasattr(field_type, 'model_dump')
    # return FieldInfo(field_name=field_name, field_type=field_type, by_reference=by_reference, is_list=is_list, has_model_dump=has_model_dump)

# def field_infos(cls: BaseModel, field_name: str):
#     info = cls.model_fields[field_name].annotation
#     is_list = False
#     if get_origin(info) is Union:
#         field_type = get_args(info)[0]
#         by_reference = '_id' in get_args(get_args(info)[1])
#     elif get_origin(info) is list:
#         field_type = get_args(info)[0]
#         by_reference = False
#         is_list = True
#         info = field_type
#         if get_origin(info) is Union:
#             field_type = get_args(field_type)[0]
#             by_reference = '_id' in get_args(get_args(info)[1])
#     else:
#         field_type = info
#         by_reference = False
#     has_model_dump = hasattr(field_type, 'model_dump')
#     return FieldInfo(field_name=field_name, field_type=field_type, by_reference=by_reference, is_list=is_list, has_model_dump=has_model_dump)


def recursive_field_infos(field_info: FieldInfo, path: list):
    if field_info.has_model_dump:
        for key in field_info.field_type.model_fields.keys():
            path.append(key)
            path_str = '.'.join(path)
            field_info_to_set: FieldInfo = field_infos(cls=field_info.field_type, field_name=key)
            field_info_to_set.field_name = path_str
            setattr(field_info, key, field_info_to_set)
            recursive_field_infos(field_info=getattr(field_info, key), path=path)
    path.pop(-1)
    return field_info


def set_new_field_info(cls: BaseModel):
    for key in cls.model_fields.keys():
        field_info: FieldInfo = field_infos(cls=cls, field_name=key)
        recursive_field_infos(field_info=field_info, path=[field_info.field_name])
        setattr(cls, key, field_info)


def resolve_indexes(cls: BaseModel):
    indexes = []
    text_keys = []
    for key in cls.model_fields.keys():
        is_index = cls.model_fields[key]._attributes_set.get('index') or False
        is_unique = cls.model_fields[key]._attributes_set.get('unique') or False
        is_text_index = cls.model_fields[key]._attributes_set.get('text_index') or False
        if is_index:
            indexes.append(IndexModel(
                [(key, ASCENDING)], name=key, unique=is_unique))
        if is_text_index:
            text_keys.append((key, TEXT))
    if len(text_keys) > 0:
        indexes.append(
            IndexModel(text_keys, name='texts', default_language='portuguese')
        )
    return indexes


def resolve_lookup_and_set(cls: BaseModel, pipeline: list, path: list):
    for key in cls.model_fields.keys():
        field_info: FieldInfo = field_infos(cls=cls, field_name=key)
        has_model_dump = field_info.has_model_dump
        by_reference = field_info.by_reference
        field_type = field_info.field_type
        is_list = field_info.is_list
        if has_model_dump:
            path.append(key)
            path_str = '.'.join(path)
            if by_reference:
                collection = field_type._collection
                pipeline += lookup_and_set(from_=collection,
                                           local_field=path_str,
                                           foreign_field='_id',
                                           as_=path_str,
                                           is_reference_list=is_list)
            if not is_list:
                resolve_lookup_and_set(
                    cls=field_type, pipeline=pipeline, path=path)
            path.pop(-1)
    return pipeline
