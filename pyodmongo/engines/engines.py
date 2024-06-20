from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, UpdateMany, DeleteOne, DeleteMany
from pymongo.results import BulkWriteResult
from datetime import datetime, timezone
from bson import ObjectId
from bson.codec_options import CodecOptions
from ..models.db_model import DbModel
from ..models.id_model import Id
from ..models.responses import DbResponse
from ..models.query_operators import QueryOperator
from ..models.sort_operators import SortOperator
from ..models.paginate import ResponsePaginate
from ..models.db_field_info import DbField
from typing import TypeVar, Type, Union
from concurrent.futures import ThreadPoolExecutor
from .utils import consolidate_dict, mount_base_pipeline
from ..services.verify_subclasses import is_subclass
from asyncio import gather
from math import ceil


Model = TypeVar("Model", bound=DbModel)


class _Engine:
    """
    Base class for database operations, providing common functionality for both synchronous and asynchronous engines.

    Attributes:
        _client (MongoClient): The MongoDB client.
        _db (Database): The database instance.
        _tz_info (timezone): The timezone information.
    """

    def __init__(self, Client, mongo_uri, db_name, tz_info: timezone = None):
        """
        Initialize the database engine.

        Args:
            Client (type): The MongoDB client class.
            mongo_uri (str): The MongoDB URI.
            db_name (str): The database name.
            tz_info (timezone, optional): The timezone information. Defaults to None.
        """
        self._client = Client(mongo_uri)
        self._db = self._client[db_name]
        self._tz_info = tz_info

    def _query(self, query: QueryOperator, raw_query: dict) -> dict:
        """
        Construct a query dictionary from a QueryOperator or a raw query.

        Args:
            query (QueryOperator): The query operator.
            raw_query (dict): The raw query dictionary.

        Returns:
            dict: The constructed query dictionary.
        """
        if not is_subclass(class_to_verify=query.__class__, subclass=QueryOperator):
            raise TypeError(
                'query argument must be a valid query operator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        raw_query = {} if not raw_query else raw_query
        return query.to_dict() if query else raw_query

    def _sort(self, sort: QueryOperator, raw_sort: dict) -> dict:
        """
        Construct a sort dictionary from a SortOperator or a raw sort.

        Args:
            sort (QueryOperator): The sort operator.
            raw_sort (dict): The raw sort dictionary.

        Returns:
            dict: The constructed sort dictionary.
        """
        if sort and (type(sort) != SortOperator):
            raise TypeError(
                'sort argument must be a SortOperator from pyodmongo.queries. If you really need to make a very specific sort, use "raw_sort" argument'
            )
        raw_sort = {} if not raw_sort else raw_sort
        return sort.to_dict() if sort else raw_sort

    def _set_tz_info(self, tz_info: timezone):
        """
        Set the timezone information.

        Args:
            tz_info (timezone): The timezone information.

        Returns:
            timezone: The set timezone information.
        """
        return tz_info if tz_info else self._tz_info

    def _update_many_operation(self, obj: Type[Model], query_dict: dict, now):
        """
        Create an UpdateMany operation for bulk updates.

        Args:
            obj (DbModel): The database model object.
            query_dict (dict): The query dictionary.
            now (datetime): The current datetime.

        Returns:
            UpdateMany: The UpdateMany operation.
        """
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

    def _create_delete_operations_list(
        self, query: QueryOperator, raw_query: dict, delete_one: bool
    ):
        """
        Create a list of delete operations.

        Args:
            query (QueryOperator): The query operator.
            raw_query (dict): The raw query dictionary.
            delete_one (bool): Flag to indicate whether to delete one or many documents.

        Returns:
            list: The list of delete operations.
        """
        query = self._query(query=query, raw_query=raw_query)
        if delete_one:
            return [DeleteOne(filter=query)]
        return [DeleteMany(filter=query)]

    def _create_save_operations_list(
        self,
        objs: list[Type[Model]],
        query: QueryOperator,
        raw_query: dict,
    ):
        """
        Create lists of indexes and save operations for bulk writes.

        Args:
            objs (list[DbModel]): The list of database model objects.
            query (QueryOperator): The query operator.
            raw_query (dict): The raw query dictionary.

        Returns:
            tuple: A tuple containing indexes, operations, and the current datetime.
        """
        operations = {}
        indexes = {}
        query = self._query(query=query, raw_query=raw_query)
        now = datetime.now(self._tz_info)
        now = now.replace(microsecond=int(now.microsecond / 1000) * 1000)
        for obj in objs:
            obj: Model
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
        self, result: BulkWriteResult, objs: list[Model], collection_name: str, now
    ):
        """
        Perform post-save operations.

        Args:
            result (BulkWriteResult): The bulk write result.
            objs (list[DbModel]): The list of database model objects.
            collection_name (str): The name of the collection.
            now (datetime): The current datetime.
        """
        objs_from_collection = list(
            filter(lambda x: x._collection == collection_name, objs)
        )
        for index, obj_id in result.upserted_ids.items():
            objs_from_collection[index].id = Id(obj_id)
            objs_from_collection[index].created_at = now
            objs_from_collection[index].updated_at = now

    def _db_response(self, result: BulkWriteResult):
        """
        Create a database response object from a bulk write result.

        Args:
            result (BulkWriteResult): The bulk write result.

        Returns:
            DbResponse: The database response object.
        """
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
        Model: Type[Model],
        pipeline,
        tz_info: timezone,
    ):
        """
        Create an aggregation cursor with the specified pipeline and timezone information.

        Args:
            Model (DbModel): The database model class.
            pipeline (list): The aggregation pipeline.
            tz_info (timezone): The timezone information.

        Returns:
            CommandCursor: The aggregation cursor.
        """
        tz_info = self._set_tz_info(tz_info=tz_info)
        tz_aware = True if tz_info else False
        collection = self._db[Model._collection].with_options(
            codec_options=CodecOptions(tz_aware=tz_aware, tzinfo=tz_info)
        )
        return collection.aggregate(pipeline)

    def _aggregate_pipeline(
        self,
        Model: Type[Model],
        query: QueryOperator,
        raw_query: dict,
        sort: SortOperator,
        raw_sort: dict,
        populate: bool,
        populate_db_fields: list[DbField] | None,
    ) -> dict:
        """
        Construct an aggregation pipeline.

        Args:
            Model (DbModel): The database model class.
            query (QueryOperator): The query operator.
            raw_query (dict): The raw query dictionary.
            sort (SortOperator): The sort operator.
            raw_sort (dict): The raw sort dictionary.
            populate (bool): Flag to indicate whether to populate related documents.

        Returns:
            tuple: A tuple containing the pipeline, query, and sort dictionaries.
        """
        query = self._query(query=query, raw_query=raw_query)
        sort = self._sort(sort=sort, raw_sort=raw_sort)
        return (
            mount_base_pipeline(
                Model=Model,
                query=query,
                sort=sort,
                populate=populate,
                populate_db_fields=populate_db_fields,
            ),
            query,
            sort,
        )

    def _add_paginate_to_pipeline(
        self, pipeline: list, current_page: int, docs_per_page: int
    ):
        """
        Add pagination stages to the aggregation pipeline.

        Args:
            pipeline (list): The aggregation pipeline.
            current_page (int): The current page number.
            docs_per_page (int): The number of documents per page.
        """
        max_docs_per_page = 1000
        current_page = 1 if current_page <= 0 else current_page
        docs_per_page = (
            max_docs_per_page if docs_per_page > max_docs_per_page else docs_per_page
        )
        skip = (docs_per_page * current_page) - docs_per_page
        skip_stage = [{"$skip": skip}]
        limit_stage = [{"$limit": docs_per_page}]
        pipeline += skip_stage + limit_stage


class AsyncDbEngine(_Engine):
    """
    Asynchronous database engine class that extends the base engine to provide asynchronous operations.
    """

    def __init__(self, mongo_uri, db_name, tz_info: timezone = None):
        """
        Initialize the asynchronous database engine.

        Args:
            mongo_uri (str): The MongoDB URI.
            db_name (str): The database name.
            tz_info (timezone, optional): The timezone information. Defaults to None.
        """
        super().__init__(
            Client=AsyncIOMotorClient,
            mongo_uri=mongo_uri,
            db_name=db_name,
            tz_info=tz_info,
        )

    async def save_all(self, obj_list: list[Model]) -> dict[str, DbResponse]:
        """
        Save a list of objects to the database.

        Args:
            obj_list (list[DbModel]): The list of database model objects.
        """
        response = {}
        indexes, operations, now = self._create_save_operations_list(
            objs=obj_list, query=None, raw_query=None
        )
        for collection_name, index_list in indexes.items():
            if index_list:
                await self._db[collection_name].create_indexes(index_list)
        for collection_name, operation_list in operations.items():
            result: BulkWriteResult = await self._db[collection_name].bulk_write(
                operation_list
            )
            self._after_save(
                result=result, objs=obj_list, collection_name=collection_name, now=now
            )
            response[collection_name] = self._db_response(result=result)
        return response

    async def save(
        self, obj: Model, query: QueryOperator = None, raw_query: dict = None
    ) -> DbResponse:
        """
        Save a single object to the database.

        Args:
            obj (DbModel): The database model object.
            query (QueryOperator, optional): The query operator. Defaults to None.
            raw_query (dict, optional): The raw query dictionary. Defaults to None.

        Returns:
            DbResponse: The database response object.
        """
        indexes, operations, now = self._create_save_operations_list(
            objs=[obj], query=query, raw_query=raw_query
        )
        collection_name = obj._collection
        index_list = indexes[collection_name]
        if index_list:
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
        Model: Type[Model],
        query: QueryOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        populate_db_fields: list[DbField] | None = None,
        as_dict: bool = False,
        tz_info: timezone = None,
    ) -> Model:
        """
        Find a single document in the database.

        Args:
            Model (DbModel): The database model class.
            query (QueryOperator, optional): The query operator. Defaults to None.
            raw_query (dict, optional): The raw query dictionary. Defaults to None.
            sort (SortOperator, optional): The sort operator. Defaults to None.
            raw_sort (dict, optional): The raw sort dictionary. Defaults to None.
            populate (bool, optional): Flag to indicate whether to populate related documents. Defaults to False.
            as_dict (bool, optional): Flag to return the result as a dictionary. Defaults to False.
            tz_info (timezone, optional): The timezone information. Defaults to None.

        Returns:
            DbModel: The found database model object.
        """
        pipeline, _, _ = self._aggregate_pipeline(
            Model=Model,
            query=query,
            raw_query=raw_query,
            sort=sort,
            raw_sort=raw_sort,
            populate=populate,
            populate_db_fields=populate_db_fields,
        )
        pipeline += [{"$limit": 1}]
        cursor = self._aggregate_cursor(Model=Model, pipeline=pipeline, tz_info=tz_info)
        if as_dict:
            result = await cursor.to_list(length=None)
        else:
            result = [Model(**doc) async for doc in cursor]
        try:
            return result[0]
        except IndexError:
            return None

    async def find_many(
        self,
        Model: Type[Model],
        query: QueryOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        populate_db_fields: list[DbField] | None = None,
        as_dict: bool = False,
        tz_info: timezone = None,
        paginate: bool = False,
        current_page: int = 1,
        docs_per_page: int = 1000,
    ) -> Union[list[Model], ResponsePaginate]:
        """
        Find multiple documents in the database.

        Args:
            Model (DbModel): The database model class.
            query (QueryOperator, optional): The query operator. Defaults to None.
            raw_query (dict, optional): The raw query dictionary. Defaults to None.
            sort (SortOperator, optional): The sort operator. Defaults to None.
            raw_sort (dict, optional): The raw sort dictionary. Defaults to None.
            populate (bool, optional): Flag to indicate whether to populate related documents. Defaults to False.
            as_dict (bool, optional): Flag to return the results as dictionaries. Defaults to False.
            tz_info (timezone, optional): The timezone information. Defaults to None.
            paginate (bool, optional): Flag to enable pagination. Defaults to False.
            current_page (int, optional): The current page number. Defaults to 1.
            docs_per_page (int, optional): The number of documents per page. Defaults to 1000.

        Returns:
            list[DbModel] or ResponsePaginate: The list of found database model objects or a paginated response.
        """
        pipeline, query, _ = self._aggregate_pipeline(
            Model=Model,
            query=query,
            raw_query=raw_query,
            sort=sort,
            raw_sort=raw_sort,
            populate=populate,
            populate_db_fields=populate_db_fields,
        )

        async def _result():
            cursor = self._aggregate_cursor(
                Model=Model, pipeline=pipeline, tz_info=tz_info
            )
            if as_dict:
                result = await cursor.to_list(length=None)
            else:
                result = [Model(**doc) async for doc in cursor]
            return result

        if not paginate:
            return await _result()
        self._add_paginate_to_pipeline(
            pipeline=pipeline, current_page=current_page, docs_per_page=docs_per_page
        )
        cursor = self._aggregate_cursor(Model=Model, pipeline=pipeline, tz_info=tz_info)

        async def _count():
            kwargs = {"hint": "_id_"} if not query else {}
            return await self._db[Model._collection].count_documents(
                filter=query, **kwargs
            )

        result, count = await gather(_result(), _count())
        page_quantity = ceil(count / docs_per_page)
        return ResponsePaginate(
            current_page=current_page,
            page_quantity=page_quantity,
            docs_quantity=count,
            docs=result,
        )

    async def delete(
        self,
        Model: Type[Model],
        query: QueryOperator = None,
        raw_query: dict = None,
        delete_one: bool = False,
    ) -> DbResponse:
        """
        Delete documents from the database.

        Args:
            Model (DbModel): The database model class.
            query (QueryOperator, optional): The query operator. Defaults to None.
            raw_query (dict, optional): The raw query dictionary. Defaults to None.
            delete_one (bool, optional): Flag to delete a single document. Defaults to False.

        Returns:
            DbResponse: The database response object.
        """
        operations = self._create_delete_operations_list(
            query=query, raw_query=raw_query, delete_one=delete_one
        )
        collection_name = Model._collection
        result: BulkWriteResult = await self._db[collection_name].bulk_write(operations)
        return self._db_response(result=result)


class DbEngine(_Engine):
    """
    Synchronous database engine class that extends the base engine to provide synchronous operations.
    """

    def __init__(self, mongo_uri, db_name, tz_info: timezone = None):
        """
        Initialize the synchronous database engine.

        Args:
            mongo_uri (str): The MongoDB URI.
            db_name (str): The database name.
            tz_info (timezone, optional): The timezone information. Defaults to None.
        """
        super().__init__(
            Client=MongoClient,
            mongo_uri=mongo_uri,
            db_name=db_name,
            tz_info=tz_info,
        )

    def save_all(self, obj_list: list[Model]) -> dict[str, DbResponse]:
        """
        Save a list of objects to the database.

        Args:
            obj_list (list[DbModel]): The list of database model objects.
        """
        response = {}
        indexes, operations, now = self._create_save_operations_list(
            objs=obj_list, query=None, raw_query=None
        )
        for collection_name, index_list in indexes.items():
            if index_list:
                self._db[collection_name].create_indexes(index_list)
        for collection_name, operation_list in operations.items():
            result: BulkWriteResult = self._db[collection_name].bulk_write(
                operation_list
            )
            self._after_save(
                result=result, objs=obj_list, collection_name=collection_name, now=now
            )
            response[collection_name] = self._db_response(result=result)
        return response

    def save(
        self, obj: Model, query: QueryOperator = None, raw_query: dict = None
    ) -> DbResponse:
        """
        Save a single object to the database.

        Args:
            obj (DbModel): The database model object.
            query (QueryOperator, optional): The query operator. Defaults to None.
            raw_query (dict, optional): The raw query dictionary. Defaults to None.

        Returns:
            DbResponse: The database response object.
        """
        indexes, operations, now = self._create_save_operations_list(
            objs=[obj], query=query, raw_query=raw_query
        )
        collection_name = obj._collection
        index_list = indexes[collection_name]
        if index_list:
            self._db[collection_name].create_indexes(index_list)
        operation_list = operations[collection_name]
        result: BulkWriteResult = self._db[collection_name].bulk_write(operation_list)
        self._after_save(
            result=result, objs=[obj], collection_name=collection_name, now=now
        )
        return self._db_response(result=result)

    def find_one(
        self,
        Model: Type[Model],
        query: QueryOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        populate_db_fields: list[DbField] | None = None,
        as_dict: bool = False,
        tz_info: timezone = None,
    ) -> Model:
        """
        Find a single document in the database.

        Args:
            Model (DbModel): The database model class.
            query (QueryOperator, optional): The query operator. Defaults to None.
            raw_query (dict, optional): The raw query dictionary. Defaults to None.
            sort (SortOperator, optional): The sort operator. Defaults to None.
            raw_sort (dict, optional): The raw sort dictionary. Defaults to None.
            populate (bool, optional): Flag to indicate whether to populate related documents. Defaults to False.
            as_dict (bool, optional): Flag to return the result as a dictionary. Defaults to False.
            tz_info (timezone, optional): The timezone information. Defaults to None.

        Returns:
            DbModel: The found database model object.
        """
        pipeline, _, _ = self._aggregate_pipeline(
            Model=Model,
            query=query,
            raw_query=raw_query,
            sort=sort,
            raw_sort=raw_sort,
            populate=populate,
            populate_db_fields=populate_db_fields,
        )
        pipeline += [{"$limit": 1}]
        cursor = self._aggregate_cursor(Model=Model, pipeline=pipeline, tz_info=tz_info)
        if as_dict:
            result = list(cursor)
        else:
            result = [Model(**doc) for doc in cursor]
        try:
            return result[0]
        except IndexError:
            return None

    def find_many(
        self,
        Model: Type[Model],
        query: QueryOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        populate_db_fields: list[DbField] | None = None,
        as_dict: bool = False,
        tz_info: timezone = None,
        paginate: bool = False,
        current_page: int = 1,
        docs_per_page: int = 1000,
    ) -> Union[list[Model], ResponsePaginate]:
        """
        Find multiple documents in the database.

        Args:
            Model (DbModel): The database model class.
            query (QueryOperator, optional): The query operator. Defaults to None.
            raw_query (dict, optional): The raw query dictionary. Defaults to None.
            sort (SortOperator, optional): The sort operator. Defaults to None.
            raw_sort (dict, optional): The raw sort dictionary. Defaults to None.
            populate (bool, optional): Flag to indicate whether to populate related documents. Defaults to False.
            as_dict (bool, optional): Flag to return the results as dictionaries. Defaults to False.
            tz_info (timezone, optional): The timezone information. Defaults to None.
            paginate (bool, optional): Flag to enable pagination. Defaults to False.
            current_page (int, optional): The current page number. Defaults to 1.
            docs_per_page (int, optional): The number of documents per page. Defaults to 1000.

        Returns:
            list[DbModel] or ResponsePaginate: The list of found database model objects or a paginated response.
        """
        pipeline, query, _ = self._aggregate_pipeline(
            Model=Model,
            query=query,
            raw_query=raw_query,
            sort=sort,
            raw_sort=raw_sort,
            populate=populate,
            populate_db_fields=populate_db_fields,
        )

        def _result():
            cursor = self._aggregate_cursor(
                Model=Model, pipeline=pipeline, tz_info=tz_info
            )
            if as_dict:
                result = list(cursor)
            else:
                result = [Model(**doc) for doc in cursor]
            return result

        if not paginate:
            return _result()
        self._add_paginate_to_pipeline(
            pipeline=pipeline, current_page=current_page, docs_per_page=docs_per_page
        )
        cursor = self._aggregate_cursor(Model=Model, pipeline=pipeline, tz_info=tz_info)

        def _count():
            kwargs = {"hint": "_id_"} if not query else {}
            return self._db[Model._collection].count_documents(filter=query, **kwargs)

        with ThreadPoolExecutor() as executor:
            future_result = executor.submit(_result)
            future_count = executor.submit(_count)
            result = future_result.result()
            count = future_count.result()

        page_quantity = ceil(count / docs_per_page)
        return ResponsePaginate(
            current_page=current_page,
            page_quantity=page_quantity,
            docs_quantity=count,
            docs=result,
        )

    def delete(
        self,
        Model: Type[Model],
        query: QueryOperator = None,
        raw_query: dict = None,
        delete_one: bool = False,
    ) -> DbResponse:
        """
        Delete documents from the database.

        Args:
            Model (DbModel): The database model class.
            query (QueryOperator, optional): The query operator. Defaults to None.
            raw_query (dict, optional): The raw query dictionary. Defaults to None.
            delete_one (bool, optional): Flag to delete a single document. Defaults to False.

        Returns:
            DbResponse: The database response object.
        """
        operations = self._create_delete_operations_list(
            query=query, raw_query=raw_query, delete_one=delete_one
        )
        collection_name = Model._collection
        result: BulkWriteResult = self._db[collection_name].bulk_write(operations)
        return self._db_response(result=result)
