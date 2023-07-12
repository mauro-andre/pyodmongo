from bson import ObjectId
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
from .connection import db


async def __save_dict(dict_to_save: dict, collection, indexes):
    find_filter = {'_id': ObjectId(dict_to_save.get('id'))}
    now = datetime.utcnow()
    dict_to_save['updated_at'] = now
    dict_to_save.pop('id')
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


async def save(obj):
    dict_to_save = {}
    for key, field_prop in obj.__fields__.items():
        attr_has_id = hasattr(field_prop.type_, 'id')
        try:
            attr_value = getattr(obj, key).dict()
            by_reference = obj.__fields__[
                key].field_info.extra.get('by_reference')
            if by_reference and attr_has_id:
                attr_value = attr_value.get('id')
        except AttributeError:
            attr_value = getattr(obj, key)
        dict_to_save[key] = attr_value
    await __save_dict(dict_to_save=dict_to_save, collection=db[obj._collection], indexes=obj._indexes)
