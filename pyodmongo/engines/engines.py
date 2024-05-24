from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, UpdateMany
from pymongo.results import BulkWriteResult
from datetime import datetime, timezone, UTC
from bson import ObjectId
from ..models.db_model import DbModel
from ..models.query_operators import QueryOperator
from ..engine.utils import consolidate_dict, mount_base_pipeline


class _Engine:
    def __init__(self, Client, mongo_uri, db_name, tz_info: timezone = None):
        self._client = Client(mongo_uri)
        self._db = self._client[db_name]
        self._tz_info = tz_info

    def _update_many_operation(self, obj: DbModel, query_dict: dict, now):
        dct = consolidate_dict(obj=obj, dct={})
        find_filter = query_dict or {"_id": ObjectId(dct.get("_id"))}
        dct[obj.__class__.updated_at.field_alias] = now
        dct.pop("_id")
        dct.pop(obj.__class__.created_at.field_alias)
        to_save = {
            "$set": dct,
            "$setOnInsert": {obj.__class__.created_at.field_alias: now},
        }
        return UpdateMany(filter=find_filter, update=to_save, upsert=True)

    def _create_operations_list(
        self,
        objs: list[DbModel],
        query: QueryOperator,
        raw_query: dict,
    ):
        operations = {}
        indexes = {}
        raw_query = {} if not raw_query else raw_query
        query = query.to_dict() if query else raw_query
        now = datetime.now(self._tz_info)
        now = now.replace(microsecond=int(now.microsecond / 1000) * 1000)
        for obj in objs:
            obj: DbModel
            operation = self._update_many_operation(obj=obj, query_dict=query, now=now)
            collection_name = obj._collection
            try:
                operations[collection_name] += [operation]
            except KeyError:
                operations[collection_name] = [operation]

            try:
                obj_indexes = obj._indexes
            except AttributeError:
                obj_indexes = obj._init_indexes
            indexes[collection_name] = obj_indexes
        return indexes, operations, now

    def _after_save(
        self, result: BulkWriteResult, objs: list[DbModel], collection_name: str, now
    ):
        objs_from_collection = list(
            filter(lambda x: x._collection == collection_name, objs)
        )
        for index, obj_id in result.upserted_ids.items():
            objs_from_collection[index].id = obj_id
            objs_from_collection[index].created_at = now
            objs_from_collection[index].updated_at = now


class AsyncDbEngine(_Engine):
    def __init__(self, mongo_uri, db_name, tz_info: timezone = None):
        super().__init__(
            Client=AsyncIOMotorClient,
            mongo_uri=mongo_uri,
            db_name=db_name,
            tz_info=tz_info,
        )

    async def save_all(self, objs: list[DbModel]):
        indexes, operations, now = self._create_operations_list(
            objs=objs, query=None, raw_query=None
        )
        for collection_name, index_list in indexes.items():
            await self._db[collection_name].create_indexes(index_list)
        for collection_name, operation_list in operations.items():
            result: BulkWriteResult = await self._db[collection_name].bulk_write(
                operation_list
            )
            self._after_save(
                result=result, objs=objs, collection_name=collection_name, now=now
            )


class DbEngine(_Engine):
    def __init__(self, mongo_uri, db_name, tz_info: timezone = None):
        super().__init__(
            Client=MongoClient,
            mongo_uri=mongo_uri,
            db_name=db_name,
            tz_info=tz_info,
        )

    def save_all(self, objs: list[DbModel]):
        indexes, operations, now = self._create_operations_list(
            objs=objs, query=None, raw_query=None
        )
        for collection_name, index_list in indexes.items():
            self._db[collection_name].create_indexes(index_list)
        for collection_name, operation_list in operations.items():
            result: BulkWriteResult = self._db[collection_name].bulk_write(
                operation_list
            )
            self._after_save(
                result=result, objs=objs, collection_name=collection_name, now=now
            )
