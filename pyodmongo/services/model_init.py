from ..pydantic_mod.main import BaseModel
from pymongo import IndexModel, ASCENDING, TEXT
from typing import Any, Union, get_origin, get_args
from types import UnionType
from ..models.id_model import Id
from ..models.db_field_info import DbFieldInfo
from .aggregate_stages import lookup_and_set
# from typing import get_origin, get_args
# from ..models.db_field_info import DbFieldInfo
# from ..models.id_model import Id
# from ..models.base import Base
# from pprint import pprint


# def _is_union(field_type):
#     info = get_origin(field_type)
#     return info is UnionType or info is Union


# def _union_fields(field_type):
#     by_reference = Id in field_type.__args__
#     field_type_index = 0
#     if by_reference:
#         id_index = field_type.__args__.index(Id)
#         field_type_index = abs(id_index - 1)
#     return by_reference, field_type.__args__[field_type_index]


# def _is_list(field_type):
#     info = get_origin(field_type)
#     return info is list


# def field_infos(field_name: str, field_type: Any, path: list):
#     by_reference = False
#     is_list = False
#     if _is_union(field_type):
#         by_reference, field_type = _union_fields(field_type)
#     elif _is_list(field_type):
#         is_list = True
#         if _is_union(field_type.__args__[0]):
#             by_reference, field_type = _union_fields(field_type.__args__[0])
#     is_pyodmongo_model = hasattr(field_type, '__is_pyodmongo_model__')
#     field_info = DbFieldInfo(field_name=field_name,
#                      field_type=field_type,
#                      by_reference=by_reference,
#                      is_list=is_list,
#                      is_pyodmongo_model=is_pyodmongo_model)
#     if is_pyodmongo_model:
#         for rec_field_name, rec_field_type in field_type.__model_fields__().items():
#             path.append(rec_field_name)
#             path_str = '.'.join(path)
#             rec_field_info: DbFieldInfo = field_infos(field_name=rec_field_name, field_type=rec_field_type, path=path)
#             rec_field_info.field_name = path_str
#             setattr(field_info, rec_field_name, rec_field_info)
#     path.pop(-1)
#     return field_info

# def field_infos(base: Base, path: list):
#     field_name = base.field_name
#     field_type = base.field_type
#     by_reference = False
#     is_list = False
#     if _is_union(field_type):
#         by_reference, field_type = _union_fields(field_type)
#     elif _is_list(field_type):
#         is_list = True
#         if _is_union(field_type.__args__[0]):
#             by_reference, field_type = _union_fields(field_type.__args__[0])
#     is_pyodmongo_model = hasattr(field_type, '__is_pyodmongo_model__')
#     field_info = DbFieldInfo(field_name=field_name,
#                              field_type=field_type,
#                              by_reference=by_reference,
#                              is_list=is_list,
#                              is_pyodmongo_model=is_pyodmongo_model,
#                              default_value=base.default_value)
############################################################
# print(base)
# if is_pyodmongo_model: #TODO this method will not work with a simple BaseModel without reference (Not base in MainMolde)
#     rec_bases = field_type.__model_fields__()
#     for rec_base in rec_bases:
#         rec_base: Base
#         path.append(rec_base.field_name)
#         path_str = '.'.join(path)
#         rec_field_info: DbFieldInfo = field_infos(base=rec_base, path=path)
#         rec_field_info.field_name = path_str
#         setattr(field_info, rec_base.field_name, rec_field_info)
#     # for rec_field_name, rec_field_type in field_type.__model_fields__().items():
#     #     path.append(rec_field_name)
#     #     path_str = '.'.join(path)
#     #     rec_field_info: DbFieldInfo = field_infos(field_name=rec_field_name, field_type=rec_field_type, path=path)
#     #     rec_field_info.field_name = path_str
#     #     setattr(field_info, rec_field_name, rec_field_info)
# path.pop(-1)
# return field_info


# def recursive_field_infos(field_info: FieldInfo, path: list):
#     if field_info.is_pyodmongo_model:
#         for key in field_info.field_type.model_fields.keys():
#             path.append(key)
#             path_str = '.'.join(path)
#             field_info_to_set: FieldInfo = field_infos(cls=field_info.field_type, field_name=key)
#             field_info_to_set.field_name = path_str
#             setattr(field_info, key, field_info_to_set)
#             recursive_field_infos(field_info=getattr(field_info, key), path=path)
#     path.pop(-1)
#     return field_info


# def set_new_field_info(cls: BaseModel):
#     for key in cls.model_fields.keys():
#         field_info: FieldInfo = field_infos(cls=cls, field_name=key)
#         recursive_field_infos(field_info=field_info, path=[field_info.field_name])
#         setattr(cls, key, field_info)

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


def _is_union(field_type: Any):
    return get_origin(field_type) is UnionType or get_origin(field_type) is Union


def _union_collector_info(args):
    args = get_args(args)
    by_reference = Id in args
    if by_reference:
        id_index = args.index(Id)
        field_type_index = int(abs(id_index - 1))
        field_type = args[field_type_index]
    else:
        field_type = args[0]
    return field_type, by_reference


def _field_annotation_infos(field_annotation: Any):
    by_reference = False
    field_type = field_annotation
    is_list = get_origin(field_annotation) is list
    if is_list:
        args = get_args(field_annotation)[0]
        is_union = _is_union(args)
        if is_union:
            field_type, by_reference = _union_collector_info(args=args)
        else:
            field_type = args
    elif _is_union(field_annotation):
        field_type, by_reference = _union_collector_info(args=field_annotation)
    has_model_fields = hasattr(field_type, 'model_fields')
    return field_type, by_reference, is_list, has_model_fields


def resolve_db_fields_and_ref_pipeline(cls: BaseModel, pipeline: list, path: list):
    for field, field_info in cls.model_fields.items():
        field_name = field
        field_alias = field_info.alias or field
        field_type, by_reference, is_list, has_model_fields = _field_annotation_infos(field_info.annotation)
        db_field_info = DbFieldInfo(field_name=field_name,
                                    field_alias=field_name,
                                    field_type=field_type,
                                    by_reference=by_reference,
                                    is_list=is_list,
                                    has_model_fields=has_model_fields)
        # db_field_info.field_alias = field_alias
        if db_field_info.has_model_fields:
            path.append(field_alias)
            path_str = '.'.join(path)
            if db_field_info.by_reference:
                collection = db_field_info.field_type._collection
                pipeline += lookup_and_set(from_=collection,
                                           local_field=path_str,
                                           foreign_field='_id',
                                           as_=path_str,
                                           is_reference_list=db_field_info.is_list)
            if not db_field_info.is_list:
                resolve_db_fields_and_ref_pipeline(cls=db_field_info.field_type,
                                                   pipeline=pipeline,
                                                   path=path)
            path.pop(-1)
    return pipeline


# def resolve_lookup_and_set(cls: BaseModel, pipeline: list, path: list):
#     for key in cls.model_fields.keys():
#         field_info: DbFieldInfo = field_infos(cls=cls, field_name=key)
#         has_model_dump = field_info.is_pyodmongo_model
#         by_reference = field_info.by_reference
#         field_type = field_info.field_type
#         is_list = field_info.is_list
#         if has_model_dump:
#             path.append(key)
#             path_str = '.'.join(path)
#             if by_reference:
#                 collection = field_type._collection
#                 pipeline += lookup_and_set(from_=collection,
#                                            local_field=path_str,
#                                            foreign_field='_id',
#                                            as_=path_str,
#                                            is_reference_list=is_list)
#             if not is_list:
#                 resolve_lookup_and_set(
#                     cls=field_type, pipeline=pipeline, path=path)
#             path.pop(-1)
#     return pipeline
