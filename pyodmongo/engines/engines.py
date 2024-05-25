from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, UpdateMany
from pymongo.results import BulkWriteResult
from datetime import datetime, timezone, UTC
from bson import ObjectId
from bson.codec_options import CodecOptions
from ..models.db_model import DbModel
from ..models.id_model import Id
from ..models.responses import DbResponse
from ..models.query_operators import QueryOperator
from ..models.sort_operators import SortOperator
from ..engine.utils import consolidate_dict, mount_base_pipeline
from ..services.verify_subclasses import is_subclass


class _Engine:
    def __init__(self, Client, mongo_uri, db_name, tz_info: timezone = None):
        self._client = Client(mongo_uri)
        self._db = self._client[db_name]
        self._tz_info = tz_info

    def _query(self, query: QueryOperator, raw_query: dict) -> dict:
        if not is_subclass(class_to_verify=query.__class__, subclass=QueryOperator):
            raise TypeError(
                'query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        raw_query = {} if not raw_query else raw_query
        return query.to_dict() if query else raw_query

    def _sort(self, sort: QueryOperator, raw_sort: dict) -> dict:
        if sort and (type(sort) != SortOperator):
            raise TypeError(
                'sort argument must be a SortOperator from pyodmongo.queries. If you really need to make a very specific sort, use "raw_sort" argument'
            )
        raw_sort = {} if not raw_sort else raw_sort
        return sort.to_dict() if sort else raw_sort

    def _set_tz_info(self, tz_info: timezone):
        return tz_info if tz_info else self._tz_info

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
        query = self._query(query=query, raw_query=raw_query)
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

    def _aggregate_cursor(
        self,
        Model: DbModel,
        pipeline,
        tz_info: timezone,
    ):
        tz_info = self._set_tz_info(tz_info=tz_info)
        tz_aware = True if tz_info else False
        collection = self._db[Model._collection].with_options(
            codec_options=CodecOptions(tz_aware=tz_aware, tzinfo=tz_info)
        )
        return collection.aggregate(pipeline)

    def _aggregate_pipeline(
        self,
        Model: DbModel,
        query: QueryOperator,
        raw_query: dict,
        sort: SortOperator,
        raw_sort: dict,
        populate: bool,
    ) -> dict:
        query = self._query(query=query, raw_query=raw_query)
        sort = self._sort(sort=sort, raw_sort=raw_sort)
        return mount_base_pipeline(
            Model=Model,
            query=query,
            sort=sort,
            populate=populate,
        )

    def _find_one_cursor(
        self,
        Model: DbModel,
        query: QueryOperator,
        raw_query: dict,
        sort: SortOperator,
        raw_sort: dict,
        populate: bool,
        tz_info: timezone,
    ):
        pipeline = self._aggregate_pipeline(
            Model=Model,
            query=query,
            raw_query=raw_query,
            sort=sort,
            raw_sort=raw_sort,
            populate=populate,
        )
        pipeline += [{"$limit": 1}]
        return self._aggregate_cursor(Model=Model, pipeline=pipeline, tz_info=tz_info)


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
    ) -> DbResponse:
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

    async def find_one(
        self,
        Model: DbModel,
        query: QueryOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        as_dict: bool = False,
        tz_info: timezone = None,
    ) -> DbModel:
        cursor = self._find_one_cursor(
            Model=Model,
            query=query,
            raw_query=raw_query,
            sort=sort,
            raw_sort=raw_sort,
            populate=populate,
            tz_info=tz_info,
        )
        if as_dict:
            result = await cursor.to_list(length=None)
        result = [Model(**doc) async for doc in cursor]
        try:
            return result[0]
        except IndexError:
            return None


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

    def save(
        self, obj: DbModel, query: QueryOperator = None, raw_query: dict = None
    ) -> DbResponse:
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

    def find_one(
        self,
        Model: DbModel,
        query: QueryOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        as_dict: bool = False,
        tz_info: timezone = None,
    ) -> DbModel:
        cursor = self._find_one_cursor(
            Model=Model,
            query=query,
            raw_query=raw_query,
            sort=sort,
            raw_sort=raw_sort,
            populate=populate,
            tz_info=tz_info,
        )
        if as_dict:
            result = cursor.to_list(length=None)
        result = [Model(**doc) for doc in cursor]
        try:
            return result[0]
        except IndexError:
            return None
