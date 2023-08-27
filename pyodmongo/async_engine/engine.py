from motor.motor_asyncio import AsyncIOMotorClient
from ..engine.utils import consolidate_dict, mount_base_pipeline
from ..models.paginate import ResponsePaginate
from ..models.query_operators import LogicalOperator, ComparisonOperator
from datetime import datetime
from bson import ObjectId
from math import ceil
from asyncio import gather


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
        result = await collection.update_many(filter=find_filter, update=to_save, upsert=True)
        return result.raw_result

    async def __aggregate(self, Model, pipeline):
        docs_cursor = self._db[Model._collection].aggregate(pipeline)
        return [Model(**doc) async for doc in docs_cursor]

    async def __resolve_count_pipeline(self, Model, pipeline):
        docs = await self._db[Model._collection].aggregate(pipeline).to_list(1)
        try:
            return docs[0]['count']
        except IndexError as e:
            return 0

    async def delete_one(self, Model, query: ComparisonOperator | LogicalOperator = None, raw_query: dict = None):
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        raw_query = {} if not raw_query else raw_query
        result = await self._db[Model._collection].delete_one(filter=query.operator_dict() if query else raw_query)
        if result.deleted_count == 0:
            {'document_deleted': 0}
        return {'document_deleted': result.deleted_count}

    # ----------END DB OPERATIONS----------

    # ---------ACTIONS----------

    async def save(self, obj, query: ComparisonOperator | LogicalOperator = None, raw_query: dict = None):
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        dct = consolidate_dict(obj=obj, dct={})
        return await self.__save_dict(dict_to_save=dct,
                                      collection=self._db[obj._collection],
                                      indexes=obj._indexes,
                                      query=query.operator_dict() if query else raw_query)

    async def save_all(self, obj_list: list):
        save_calls = [self.save(obj) for obj in obj_list]
        return await gather(*save_calls)

    async def find_one(self, Model, query: ComparisonOperator | LogicalOperator = None, raw_query: dict = None, populate: bool = False):
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        raw_query = {} if not raw_query else raw_query
        pipeline = mount_base_pipeline(Model=Model,
                                       query=query.operator_dict() if query else raw_query,
                                       populate=populate)
        pipeline += [{'$limit': 1}]
        try:
            result = await self.__aggregate(Model=Model, pipeline=pipeline)
            return result[0]
        except IndexError:
            return None

    async def find_many(self, Model, query: ComparisonOperator | LogicalOperator = None, raw_query: dict = None, populate: bool = False, current_page: int = 1, docs_per_page: int = 1000) -> ResponsePaginate:
        if query and (type(query) != ComparisonOperator and type(query) != LogicalOperator):
            raise TypeError('query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument')
        max_docs_per_page = 1000
        current_page = 1 if current_page <= 0 else current_page
        docs_per_page = max_docs_per_page if docs_per_page > max_docs_per_page else docs_per_page

        count_stage = [{'$count': 'count'}]
        skip = (docs_per_page * current_page) - docs_per_page
        skip_stage = [{'$skip': skip}]
        limit_stage = [{'$limit': docs_per_page}]

        raw_query = {} if not raw_query else raw_query
        pipeline = mount_base_pipeline(Model=Model,
                                       query=query.operator_dict() if query else raw_query,
                                       populate=populate)
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
