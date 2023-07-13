from bson import ObjectId
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
from .connection import db
from models import Integrator
from pprint import pprint


async def __save_dict(dict_to_save: dict, collection, indexes):
    find_filter = {'_id': ObjectId(dict_to_save.get('id'))}
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
        return await collection.update_one(filter=find_filter, update=to_save, upsert=True)
    except DuplicateKeyError as e:
        detail = {'message': 'duplicate key(s) error'} | {
            'keys': e.details['keyValue']}
        raise HTTPException(status_code=400, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def __consolidate_dict(obj: Integrator, dct: dict):
    for key in obj.__fields__.keys():
        value = getattr(obj, key)
        has_dict_method = hasattr(obj.__fields__[key].type_, 'dict')
        by_reference = obj.__fields__[key].field_info.extra.get('by_reference')

        if has_dict_method:
            by_reference = obj.__fields__[
                key].field_info.extra.get('by_reference')
            if type(value) != list:
                if by_reference:
                    dct[key] = value.id
                else:
                    dct[key] = {}
                    __consolidate_dict(obj=value, dct=dct[key])
            else:
                if by_reference:
                    dct[key] = [o.id for o in value]
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
    pprint(dct)
    save_result = await __save_dict(dict_to_save=dct, collection=db[obj._collection], indexes=obj._indexes)
