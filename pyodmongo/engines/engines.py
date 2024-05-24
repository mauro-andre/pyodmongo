from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, UpdateMany
from pymongo.results import BulkWriteResult
from datetime import datetime, timezone, UTC
from bson import ObjectId
from ..models.db_model import DbModel
from ..models.id_model import Id
from ..models.responses import DbResponse
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
            objs_from_collection[index].id = Id(obj_id)
            objs_from_collection[index].created_at = now
            objs_from_collection[index].updated_at = now

    def _db_response(self, result: BulkWriteResult):
        return DbResponse(
            acknowledged=result.acknowledged,
            deleted_count=result.deleted_count,
            inserted_count=result.inserted_count,
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_count=result.upserted_count,
            upserted_ids=result.upserted_ids,
        )


class AsyncDbEngine(_Engine):
    def __init__(self, mongo_uri, db_name, tz_info: timezone = None):
        super().__init__(
            Client=AsyncIOMotorClient,
            mongo_uri=mongo_uri,
            db_name=db_name,
            tz_info=tz_info,
        )

    async def save_all(self, obj_list: list[DbModel]):
        indexes, operations, now = self._create_operations_list(
            objs=obj_list, query=None, raw_query=None
        )
        for collection_name, index_list in indexes.items():
            await self._db[collection_name].create_indexes(index_list)
        for collection_name, operation_list in operations.items():
            result: BulkWriteResult = await self._db[collection_name].bulk_write(
                operation_list
            )
            self._after_save(
                result=result, objs=obj_list, collection_name=collection_name, now=now
            )

    async def save(
        self, obj: DbModel, query: QueryOperator = None, raw_query: dict = None
    ):
        indexes, operations, now = self._create_operations_list(
            objs=[obj], query=query, raw_query=raw_query
        )
        collection_name = obj._collection
        index_list = indexes[collection_name]
        await self._db[collection_name].create_indexes(index_list)
        operation_list = operations[collection_name]
        result: BulkWriteResult = await self._db[collection_name].bulk_write(
            operation_list
        )
        self._after_save(
            result=result, objs=[obj], collection_name=collection_name, now=now
        )
        return self._db_response(result=result)


class DbEngine(_Engine):
    def __init__(self, mongo_uri, db_name, tz_info: timezone = None):
        super().__init__(
            Client=MongoClient,
            mongo_uri=mongo_uri,
            db_name=db_name,
            tz_info=tz_info,
        )

    def save_all(self, obj_list: list[DbModel]):
        indexes, operations, now = self._create_operations_list(
            objs=obj_list, query=None, raw_query=None
        )
        for collection_name, index_list in indexes.items():
            self._db[collection_name].create_indexes(index_list)
        for collection_name, operation_list in operations.items():
            result: BulkWriteResult = self._db[collection_name].bulk_write(
                operation_list
            )
            self._after_save(
                result=result, objs=obj_list, collection_name=collection_name, now=now
            )

    def save(self, obj: DbModel, query: QueryOperator = None, raw_query: dict = None):
        indexes, operations, now = self._create_operations_list(
            objs=[obj], query=query, raw_query=raw_query
        )
        collection_name = obj._collection
        index_list = indexes[collection_name]
        self._db[collection_name].create_indexes(index_list)
        operation_list = operations[collection_name]
        result: BulkWriteResult = self._db[collection_name].bulk_write(operation_list)
        self._after_save(
            result=result, objs=[obj], collection_name=collection_name, now=now
        )
        return self._db_response(result=result)
