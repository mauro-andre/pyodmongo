from pymongo import MongoClient
from pymongo.results import UpdateResult, DeleteResult
from ..models.responses import SaveResponse, DeleteResponse
from ..engine.utils import consolidate_dict, mount_base_pipeline
from ..services.query_operators import query_dict, sort_dict
from ..models.paginate import ResponsePaginate
from ..models.query_operators import LogicalOperator, ComparisonOperator, SortOperator
from ..models.db_model import DbModel
from datetime import datetime
from typing import TypeVar
from bson import ObjectId
from math import ceil


Model = TypeVar("Model", bound=DbModel)


class DbEngine:
    def __init__(self, mongo_uri, db_name):
        self._client = MongoClient(mongo_uri)
        self._db = self._client[db_name]

    # ----------DB OPERATIONS----------
    def __save_dict(
        self, obj: type[Model], dict_to_save: dict, collection, indexes, query=None
    ):
        find_filter = query or {"_id": ObjectId(dict_to_save.get("_id"))}
        now = datetime.utcnow()
        now = now.replace(microsecond=int(now.microsecond / 1000) * 1000)
        dict_to_save[obj.__class__.updated_at.field_alias] = now
        dict_to_save.pop("_id")
        dict_to_save.pop(obj.__class__.created_at.field_alias)
        to_save = {
            "$set": dict_to_save,
            "$setOnInsert": {obj.__class__.created_at.field_alias: now},
        }
        if len(indexes) > 0:
            collection.create_indexes(indexes)
        result: UpdateResult = collection.update_many(
            filter=find_filter, update=to_save, upsert=True
        )
        return now, SaveResponse(
            acknowledged=result.acknowledged,
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=result.upserted_id,
            raw_result=result.raw_result,
        )

    def __aggregate(
        self, Model: type[Model], pipeline, as_dict: bool
    ) -> list[type[Model]]:
        docs_cursor = self._db[Model._collection].aggregate(pipeline)
        if as_dict:
            return list(docs_cursor)
        return [Model(**doc) for doc in docs_cursor]

    def __resolve_count_pipeline(self, Model, filter_):
        kwargs = {"hint": "_id_"} if not filter_ else {}
        return self._db[Model._collection].count_documents(filter=filter_, **kwargs)

    def delete_one(
        self,
        Model: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
    ) -> DeleteResponse:
        if query and (
            type(query) != ComparisonOperator and type(query) != LogicalOperator
        ):
            raise TypeError(
                'query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        raw_query = {} if not raw_query else raw_query
        result: DeleteResult = self._db[Model._collection].delete_one(
            filter=query_dict(query_operator=query, dct={}) if query else raw_query
        )
        return DeleteResponse(
            acknowledged=result.acknowledged,
            deleted_count=result.deleted_count,
            raw_result=result.raw_result,
        )

    def delete(
        self,
        Model: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
    ) -> DeleteResponse:
        if query and (
            type(query) != ComparisonOperator and type(query) != LogicalOperator
        ):
            raise TypeError(
                'query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        raw_query = {} if not raw_query else raw_query
        result: DeleteResult = self._db[Model._collection].delete_many(
            filter=query_dict(query_operator=query, dct={}) if query else raw_query
        )
        return DeleteResponse(
            acknowledged=result.acknowledged,
            deleted_count=result.deleted_count,
            raw_result=result.raw_result,
        )

    # ----------END DB OPERATIONS----------

    # ---------ACTIONS----------

    def save(
        self,
        obj: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
    ) -> SaveResponse:
        if query and (
            type(query) != ComparisonOperator and type(query) != LogicalOperator
        ):
            raise TypeError(
                'query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        dct = consolidate_dict(obj=obj, dct={})
        try:
            indexes = obj._indexes
        except AttributeError:
            indexes = obj._init_indexes
        now, save_response = self.__save_dict(
            obj=obj,
            dict_to_save=dct,
            collection=self._db[obj._collection],
            indexes=indexes,
            query=query_dict(query_operator=query, dct={}) if query else raw_query,
        )
        if save_response.upserted_id:
            obj.id = save_response.upserted_id
            obj.created_at = now
            obj.updated_at = now
        return save_response

    def save_all(self, obj_list: list) -> list[SaveResponse]:
        result = []
        for obj in obj_list:
            result.append(self.save(obj))
        return result

    def find_one(
        self,
        Model: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        as_dict: bool = False,
    ) -> type[Model]:
        if query and (
            type(query) != ComparisonOperator and type(query) != LogicalOperator
        ):
            raise TypeError(
                'query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        if sort and (type(sort) != SortOperator):
            raise TypeError(
                'sort argument must be a SortOperator from pyodmongo.queries. If you really need to make a very specific sort, use "raw_sort" argument'
            )
        raw_query = {} if not raw_query else raw_query
        query = query_dict(query_operator=query, dct={}) if query else raw_query
        raw_sort = {} if not raw_sort else raw_sort
        sort = sort_dict(sort_operators=sort) if sort else raw_sort
        pipeline = mount_base_pipeline(
            Model=Model,
            query=query,
            sort=sort,
            populate=populate,
        )
        pipeline += [{"$limit": 1}]
        try:
            result = self.__aggregate(Model=Model, pipeline=pipeline, as_dict=as_dict)
            return result[0]
        except IndexError:
            return None

    def find_many(
        self,
        Model: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        as_dict: bool = False,
        paginate: bool = False,
        current_page: int = 1,
        docs_per_page: int = 1000,
    ):
        if query and (
            type(query) != ComparisonOperator and type(query) != LogicalOperator
        ):
            raise TypeError(
                'query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        if sort and (type(sort) != SortOperator):
            raise TypeError(
                'sort argument must be a SortOperator from pyodmongo.queries. If you really need to make a very specific sort, use "raw_sort" argument'
            )
        raw_query = {} if not raw_query else raw_query
        query = query_dict(query_operator=query, dct={}) if query else raw_query
        raw_sort = {} if not raw_sort else raw_sort
        sort = sort_dict(sort_operators=sort) if sort else raw_sort
        pipeline = mount_base_pipeline(
            Model=Model,
            query=query,
            sort=sort,
            populate=populate,
        )
        if not paginate:
            return self.__aggregate(Model=Model, pipeline=pipeline, as_dict=as_dict)
        max_docs_per_page = 1000
        current_page = 1 if current_page <= 0 else current_page
        docs_per_page = (
            max_docs_per_page if docs_per_page > max_docs_per_page else docs_per_page
        )

        skip = (docs_per_page * current_page) - docs_per_page
        skip_stage = [{"$skip": skip}]
        limit_stage = [{"$limit": docs_per_page}]

        result_pipeline = pipeline + skip_stage + limit_stage
        result = self.__aggregate(
            Model=Model, pipeline=result_pipeline, as_dict=as_dict
        )
        count = self.__resolve_count_pipeline(Model=Model, filter_=query)

        page_quantity = ceil(count / docs_per_page)
        return ResponsePaginate(
            current_page=current_page,
            page_quantity=page_quantity,
            docs_quantity=count,
            docs=result,
        )
