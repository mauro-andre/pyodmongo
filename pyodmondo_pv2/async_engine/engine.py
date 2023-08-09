from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from ..engine.utils import consolidate_dict, mount_base_pipeline
from datetime import datetime
from pprint import pprint
from bson import ObjectId
# from motor import MotorClient
# from dotenv import load_dotenv
# import os

# load_dotenv()

# MONGO_URI = os.getenv('MONGO_URI')
# MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

# client = AsyncIOMotorClient(MONGO_URI)

# db = client[MONGO_DB_NAME]

class AsyncDbEngine:
    def __init__(self, mongo_uri, db_name):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]
        
    #----------DB OPERATIONS----------
    async def __save_dict(self, dict_to_save: dict, collection, indexes):
        find_filter = {'_id': ObjectId(dict_to_save.get('_id'))}
        now = datetime.utcnow()
        dict_to_save['updated_at'] = now
        dict_to_save.pop('_id')
        dict_to_save.pop('created_at')
        to_save = {
            '$set': dict_to_save,
            '$setOnInsert': {'created_at': now}
        }
        if len(indexes) > 0:
            await collection.create_indexes(indexes)
        result = await collection.update_one(filter=find_filter, update=to_save, upsert=True)
        return result.raw_result
    
    async def __aggregate(self, Model, pipeline):
        docs_cursor = self.db[Model._collection].aggregate(pipeline)
        return [Model(**doc) async for doc in docs_cursor]
    
    #----------END DB OPERATIONS----------
    
    #---------Actions----------
    async def save(self, obj):
        dct = consolidate_dict(obj=obj, dct={})
        return await self.__save_dict(dict_to_save=dct, collection=self.db[obj._collection], indexes=obj._indexes)
    
    async def find_one(self, Model, query):
        pipeline = mount_base_pipeline(Model=Model, query=query)
        pipeline += [{'$limit': 1}]
        try:
            result = await self.__aggregate(Model=Model, pipeline=pipeline)
            return result[0]
        except IndexError:
            return None
        except TypeError as e:
            raise TypeError('no records found')
            # raise HTTPException(status_code=404, detail='no records found')
        except AttributeError as e:
            raise AttributeError(e)
            # raise HTTPException(status_code=400, detail='Id not found')
        except Exception as e:
            raise Exception(e)
            # raise HTTPException(status_code=404, detail=str(e))
        
        