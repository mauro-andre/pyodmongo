from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import UpdateResult, DeleteResult
from ..models.responses import SaveResponse, DeleteResponse
from ..engine.utils import consolidate_dict, mount_base_pipeline
from ..services.query_operators import query_dict
from ..models.paginate import ResponsePaginate
from ..models.query_operators import LogicalOperator, ComparisonOperator
from ..models.db_model import DbModel
from datetime import datetime
from typing import TypeVar
from bson import ObjectId
from math import ceil
from asyncio import gather


Model = TypeVar('Model', bound=DbModel)


class AsyncDbEngine:
    def __init__(self, mongo_uri, db_name):
        self._client = AsyncIOMotorClient(mongo_uri)
        self._db = self._client[db_name]

    # ----------DB OPERATIONS----------
    async def __save_dict(self, dict_to_save: dict, collection, indexes, query=None):
        find_filter = query or {'_id': ObjectId(dict_to_save.get('_id'))}
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
        result: UpdateResult = await collection.update_many(filter=find_filter, update=to_save, upsert=True)
        return now, SaveResponse(acknowledged=result.acknowledged,
                                 matched_count=result.matched_count,
                                 modified_count=result.modified_count,
                                 upserted_id=result.upserted_id,
                                 raw_result=result.raw_result)

    async def __aggregate(self, Model: type[Model], pipeline) -> list[type[Model]]:
        docs_cursor = self._db[Model._collection].aggregate(pipeline)
        return [Model(**doc) async for doc in docs_cursor]

    async def __resolve_count_pipeline(self, Model, pipeline):
        docs = await self._db[Model._collection].aggregate(pipeline).to_list(1)
        try:
            return docs[0]['count']
        except IndexError as e:
            return 0

    async def delete_one(self, Model: type[Model], query: ComparisonOperator | LogicalOperator = None, raw_query: dict = None) -> DeleteResponse:
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        raw_query = {} if not raw_query else raw_query
        result: DeleteResult = await self._db[Model._collection].delete_one(filter=query_dict(query_operator=query, dct={}) if query else raw_query)
        return DeleteResponse(acknowledged=result.acknowledged,
                              deleted_count=result.deleted_count,
                              raw_result=result.raw_result)

    async def delete(self, Model: type[Model], query: ComparisonOperator | LogicalOperator = None, raw_query: dict = None) -> DeleteResponse:
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        raw_query = {} if not raw_query else raw_query
        result: DeleteResult = await self._db[Model._collection].delete_many(filter=query_dict(query_operator=query, dct={}) if query else raw_query)
        return DeleteResponse(acknowledged=result.acknowledged,
                              deleted_count=result.deleted_count,
                              raw_result=result.raw_result)

    # ----------END DB OPERATIONS----------

    # ---------ACTIONS----------

    async def save(self, obj: type[Model], query: ComparisonOperator | LogicalOperator = None, raw_query: dict = None) -> SaveResponse:
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        dct = consolidate_dict(obj=obj, dct={})
        try:
            indexes = obj._indexes
        except AttributeError:
            indexes = obj._init_indexes
        now, save_response = await self.__save_dict(dict_to_save=dct,
                                                    collection=self._db[obj._collection],
                                                    indexes=indexes,
                                                    query=query_dict(query_operator=query, dct={}) if query else raw_query)
        if save_response.upserted_id:
            obj.id = save_response.upserted_id
            obj.created_at = now
            obj.updated_at = now
        return save_response

    async def save_all(self, obj_list: list) -> list[SaveResponse]:
        save_calls = [self.save(obj) for obj in obj_list]
        return await gather(*save_calls)

    async def find_one(self, Model: type[Model], query: ComparisonOperator | LogicalOperator = None, raw_query: dict = None, populate: bool = False) -> type[Model]:
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        raw_query = {} if not raw_query else raw_query
        pipeline = mount_base_pipeline(Model=Model,
                                       query=query_dict(query_operator=query, dct={}) if query else raw_query,
                                       populate=populate)
        pipeline += [{'$limit': 1}]
        try:
            result = await self.__aggregate(Model=Model, pipeline=pipeline)
            return result[0]
        except IndexError:
            return None

    async def find_many(
            self, Model: type[Model],
            query: ComparisonOperator | LogicalOperator = None,
            raw_query: dict = None, populate: bool = False,
            paginate: bool = False,
            current_page: int = 1,
            docs_per_page: int = 1000
    ):
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        pipeline = mount_base_pipeline(Model=Model,
                                       query=query_dict(query_operator=query, dct={}) if query else raw_query,
                                       populate=populate)
        if not paginate:
            return await self.__aggregate(Model=Model, pipeline=pipeline)
        max_docs_per_page = 1000
        current_page = 1 if current_page <= 0 else current_page
        docs_per_page = max_docs_per_page if docs_per_page > max_docs_per_page else docs_per_page

        count_stage = [{'$count': 'count'}]
        skip = (docs_per_page * current_page) - docs_per_page
        skip_stage = [{'$skip': skip}]
        limit_stage = [{'$limit': docs_per_page}]

        raw_query = {} if not raw_query else raw_query
        count_pipeline = pipeline + count_stage
        result_pipeline = pipeline + skip_stage + limit_stage

        result, count = await gather(
            self.__aggregate(Model=Model, pipeline=result_pipeline),
            self.__resolve_count_pipeline(Model=Model, pipeline=count_pipeline)
        )

        page_quantity = ceil(count / docs_per_page)
        return ResponsePaginate(current_page=current_page,
                                page_quantity=page_quantity,
                                docs_quantity=count,
                                docs=result)
