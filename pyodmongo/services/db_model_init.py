from pydantic import BaseModel
from pymongo import IndexModel, ASCENDING, TEXT
from .aggregate_stages import lookup_and_set
from typing import get_origin, get_args
from ..models.id_model import Id
from ..models.field_info import FieldInfo


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
    field_info = FieldInfo(field_name=field_name, field_type=field_type, by_reference=by_reference, is_list=is_list,
                           has_dict_method=has_dict_method)
    return field_info


def recursive_field_infos(cls: BaseModel, field_name: str, field_info: FieldInfo, path: list):
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
    path.append(field_name)
    path_str = '.'.join(path)
    field_info.field_name = path_str
    field_info.field_type = field_type
    field_info.by_reference = by_reference
    field_info.is_list = is_list
    field_info.has_dict_method = has_dict_method
    if has_dict_method:
        for key in field_type.__fields__.keys():
            setattr(field_info, key, FieldInfo())
            print(path)
            recursive_field_infos(cls=field_type, field_name=key,
                                  field_info=getattr(field_info, key), path=path)
    path.pop(-1)
    return field_info


def set_new_field_info(cls: BaseModel):
    for key in cls.__fields__.keys():
        field_info = FieldInfo()
        recursive_field_infos(cls=cls, field_name=key,
                              field_info=field_info, path=[])
        setattr(cls, key, field_info)


def resolve_indexes(cls: BaseModel):
    indexes = []
    text_keys = []
    for key in cls.__fields__.keys():
        extra = cls.__fields__[key].field_info.extra
        if extra.get('index'):
            is_unique = False
            if extra.get('unique'):
                is_unique = True
            indexes.append(IndexModel(
                [(key, ASCENDING)], name=key, unique=is_unique))
        is_text_index = extra.get('text_index')
        if extra.get('text_index'):
            text_keys.append((key, TEXT))
    if len(text_keys) > 0:
        indexes.append(
            IndexModel(text_keys, name='texts', default_language='portuguese')
        )
    return indexes


def resolve_lookup_and_set(cls: BaseModel, pipeline: list, path: list):
    for key in cls.__fields__.keys():
        field_info: FieldInfo = field_infos(cls=cls, field_name=key)
        has_dict_method = field_info.has_dict_method
        by_reference = field_info.by_reference
        field_type = field_info.field_type
        is_list = field_info.is_list
        if has_dict_method:
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
