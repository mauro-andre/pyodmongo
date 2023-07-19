from bson import ObjectId
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
from ..services.connection import db
from ..services.db_model_init import field_infos
from ..models.field_info import FieldInfo


async def __save_dict(dict_to_save: dict, collection, indexes):
    find_filter = {'_id': ObjectId(dict_to_save.get('_id'))}
    now = datetime.utcnow()
    dict_to_save['updated_at'] = now
    dict_to_save.pop('_id')
    dict_to_save.pop('created_at')
    to_save = {
        '$set': dict_to_save,
        '$setOnInsert': {'created_at': now}
    }
    try:
        if len(indexes) > 0:
            await collection.create_indexes(indexes)
        result = await collection.update_one(filter=find_filter, update=to_save, upsert=True)
        return result.raw_result
    except DuplicateKeyError as e:
        detail = {'message': 'duplicate key(s) error'} | {
            'keys': e.details['keyValue']}
        raise HTTPException(status_code=400, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def __consolidate_dict(obj, dct: dict):
    for key in obj.__fields__.keys():
        value = getattr(obj, key)
        field_info: FieldInfo = field_infos(cls=obj, field_name=key)
        has_dict_method = field_info.has_dict_method
        is_list = field_info.is_list
        by_reference = field_info.by_reference
        # field_type, by_reference, is_list, has_dict_method = field_infos(
        #     cls=obj, field_name=key)
        if has_dict_method:
            if not is_list:
                if by_reference:
                    try:
                        dct[key] = value.id
                    except AttributeError:
                        dct[key] = value
                else:
                    dct[key] = {}
                    __consolidate_dict(obj=value, dct=dct[key])
            else:
                if by_reference:
                    try:
                        dct[key] = [o.id for o in value]
                    except AttributeError:
                        dct[key] = value
                else:
                    dct[key] = []
                    for v in value:
                        obj_lst_elem = {}
                        __consolidate_dict(obj=v, dct=obj_lst_elem)
                        dct[key].append(obj_lst_elem)
        else:
            if key == 'id':
                key = '_id'
            dct[key] = value
    return dct


async def save(obj):
    dct = __consolidate_dict(obj=obj, dct={})
    return await __save_dict(dict_to_save=dct, collection=db[obj._collection], indexes=obj._indexes)
