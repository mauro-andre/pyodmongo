from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import UpdateResult, DeleteResult
from ..models.responses import SaveResponse, DeleteResponse
from ..engine.utils import consolidate_dict, mount_base_pipeline
from ..services.query_operators import query_dict, sort_dict
from ..models.paginate import ResponsePaginate
from ..models.query_operators import LogicalOperator, ComparisonOperator
from ..models.sort_operators import SortOperator
from ..models.db_model import DbModel
from datetime import datetime, UTC, timezone
from typing import TypeVar
from bson import ObjectId
from bson.codec_options import CodecOptions
from math import ceil
from asyncio import gather


Model = TypeVar("Model", bound=DbModel)


class AsyncDbEngine:
    """
    Provides asynchronous database operations using MongoDB with the AsyncIOMotorClient.
    This class facilitates CRUD operations, supporting complex queries, aggregations,
    and pagination in an asynchronous manner to improve performance in applications
    requiring high I/O operations.

    Methods:
        __init__(mongo_uri, db_name): Initializes the AsyncIOMotorClient with the given
                                      MongoDB URI and selects the database by name.
        __save_dict(obj, dict_to_save, collection, indexes, query): Private method to
                                                                    save or update documents in the specified collection.
        __aggregate(Model, pipeline, as_dict): Private method to perform aggregation queries.
        __resolve_count_pipeline(Model, filter_): Private method to count documents based
                                                  on a filter.
        delete_one(Model, query, raw_query): Deletes a single document based on the provided query.
        delete(Model, query, raw_query): Deletes multiple documents based on the provided query.
        save(obj, query, raw_query): Saves or updates a document in the database.
        save_all(obj_list): Concurrently saves multiple documents.
        find_one(Model, query, raw_query, sort, raw_sort, populate, as_dict): Finds a single document.
        find_many(Model, query, raw_query, sort, raw_sort, populate, as_dict, paginate,
                  current_page, docs_per_page): Finds multiple documents with optional pagination.
    """

    def __init__(self, mongo_uri, db_name, tz_info: timezone = None):
        """
        Initialize the asynchronous database engine with a MongoDB connection URI and
        database name. Sets up the client and selects the specified database.

        Args:
            mongo_uri (str): MongoDB URI to connect to.
            db_name (str): Name of the database to operate on.
        """
        self._client = AsyncIOMotorClient(mongo_uri)
        self._db = self._client[db_name]
        self._tz_info = tz_info

    # ----------DB OPERATIONS----------
    async def __save_dict(
        self, obj: type[Model], dict_to_save: dict, collection, indexes, query=None
    ):
        find_filter = query or {"_id": ObjectId(dict_to_save.get("_id"))}
        now = datetime.now(UTC)
        now = now.replace(microsecond=int(now.microsecond / 1000) * 1000)
        dict_to_save[obj.__class__.updated_at.field_alias] = now
        dict_to_save.pop("_id")
        dict_to_save.pop(obj.__class__.created_at.field_alias)
        to_save = {
            "$set": dict_to_save,
            "$setOnInsert": {obj.__class__.created_at.field_alias: now},
        }
        if len(indexes) > 0:
            await collection.create_indexes(indexes)
        result: UpdateResult = await collection.update_many(
            filter=find_filter, update=to_save, upsert=True
        )
        return now, SaveResponse(
            acknowledged=result.acknowledged,
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=result.upserted_id,
            raw_result=result.raw_result,
        )

    async def __aggregate(
        self,
        Model: type[Model],
        pipeline,
        as_dict: bool,
        tz_info: timezone = None,
    ) -> list[type[Model]]:
        tz_info = tz_info if tz_info else self._tz_info
        tz_aware = True if tz_info else False
        collection = self._db[Model._collection].with_options(
            codec_options=CodecOptions(tz_aware=tz_aware, tzinfo=tz_info)
        )
        docs_cursor = collection.aggregate(pipeline)
        if as_dict:
            return await docs_cursor.to_list(length=None)
        return [Model(**doc) async for doc in docs_cursor]

    async def __resolve_count_pipeline(self, Model, filter_):
        kwargs = {"hint": "_id_"} if not filter_ else {}
        return await self._db[Model._collection].count_documents(
            filter=filter_, **kwargs
        )

    async def delete_one(
        self,
        Model: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
    ) -> DeleteResponse:
        """
        Asynchronously deletes a single document from the database based on the specified
        query or raw_query.

        Args:
            Model (type[Model]): The model class that defines the MongoDB collection.
            query (ComparisonOperator | LogicalOperator, optional): The structured query
                object.
            raw_query (dict, optional): Raw MongoDB query dictionary.

        Returns:
            DeleteResponse: A response object containing details of the delete operation.
        """
        if query and (
            type(query) != ComparisonOperator and type(query) != LogicalOperator
        ):
            raise TypeError(
                'query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        raw_query = {} if not raw_query else raw_query
        result: DeleteResult = await self._db[Model._collection].delete_one(
            filter=query_dict(query_operator=query, dct={}) if query else raw_query
        )
        return DeleteResponse(
            acknowledged=result.acknowledged,
            deleted_count=result.deleted_count,
            raw_result=result.raw_result,
        )

    async def delete(
        self,
        Model: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
    ) -> DeleteResponse:
        """
        Asynchronously deletes multiple documents from the database based on the specified
        query or raw_query.

        Args:
            Model (type[Model]): The model class that defines the MongoDB collection.
            query (ComparisonOperator | LogicalOperator, optional): The structured query
                object.
            raw_query (dict, optional): Raw MongoDB query dictionary.

        Returns:
            DeleteResponse: A response object containing details of the delete operation.
        """
        if query and (
            type(query) != ComparisonOperator and type(query) != LogicalOperator
        ):
            raise TypeError(
                'query argument must be a ComparisonOperator or LogicalOperator from pyodmongo.queries. If you really need to make a very specific query, use "raw_query" argument'
            )
        raw_query = {} if not raw_query else raw_query
        result: DeleteResult = await self._db[Model._collection].delete_many(
            filter=query_dict(query_operator=query, dct={}) if query else raw_query
        )
        return DeleteResponse(
            acknowledged=result.acknowledged,
            deleted_count=result.deleted_count,
            raw_result=result.raw_result,
        )

    # ----------END DB OPERATIONS----------

    # ---------ACTIONS----------

    async def save(
        self,
        obj: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
    ) -> SaveResponse:
        """
        Asynchronously saves or updates an object in the database. This method
        processes the object by converting it to a dictionary, applies the specified
        query for updates, and handles the indexing.

        Args:
            obj (type[Model]): The model instance to save.
            query (ComparisonOperator | LogicalOperator, optional): Query to identify the document
                for update operations.
            raw_query (dict, optional): Raw query dictionary if a more specific query is needed.

        Returns:
            SaveResponse: The result of the save operation, including details about the
                          operation's success, matched and modified counts, and any upserted ID.

        Raises:
            TypeError: If the query argument is not of type ComparisonOperator or LogicalOperator.
        """
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
        now, save_response = await self.__save_dict(
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

    async def save_all(self, obj_list: list) -> list[SaveResponse]:
        """
        Asynchronously saves multiple objects to the database concurrently. This method
        utilizes asyncio to manage concurrent save operations for efficiency.

        Args:
            obj_list (list): A list of model instances to save.

        Returns:
            list[SaveResponse]: A list of SaveResponse objects, each representing the outcome
                                of the save operation for each model instance.
        """
        save_calls = [self.save(obj) for obj in obj_list]
        return await gather(*save_calls)

    async def find_one(
        self,
        Model: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        as_dict: bool = False,
        tz_info: timezone = None,
    ) -> type[Model]:
        """
        Asynchronously finds a single document in the database that matches the specified
        query and returns it as a model instance or dictionary.

        Args:
            Model (type[Model]): The model class defining the structure of the returned object.
            query (ComparisonOperator | LogicalOperator, optional): The query to filter documents.
            raw_query (dict, optional): Raw MongoDB query if specific conditions are needed.
            sort (SortOperator, optional): Sorting instructions for the results.
            raw_sort (dict, optional): Raw sort dictionary if a specific sort is needed.
            populate (bool): Whether to populate referenced documents.
            as_dict (bool): Whether to return the document as a dictionary instead of a model instance.

        Returns:
            type[Model] | None: The found document as a model instance or dictionary, or None if no
                                 document matches the query.

        Raises:
            TypeError: If the query or sort arguments are not the correct type from pyodmongo.queries.
        """
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
            result = await self.__aggregate(
                Model=Model, pipeline=pipeline, as_dict=as_dict, tz_info=tz_info
            )
            return result[0]
        except IndexError:
            return None

    async def find_many(
        self,
        Model: type[Model],
        query: ComparisonOperator | LogicalOperator = None,
        raw_query: dict = None,
        sort: SortOperator = None,
        raw_sort: dict = None,
        populate: bool = False,
        as_dict: bool = False,
        tz_info: timezone = None,
        paginate: bool = False,
        current_page: int = 1,
        docs_per_page: int = 1000,
    ):
        """
        Asynchronously retrieves multiple documents from the database that match the specified
        query. Supports sorting, pagination, and population of references.

        Args:
            Model (type[Model]): The model class defining the structure of the documents.
            query (ComparisonOperator | LogicalOperator, optional): The query to filter documents.
            raw_query (dict, optional): Raw MongoDB query if specific conditions are needed.
            sort (SortOperator, optional): Sorting instructions for the results.
            raw_sort (dict, optional): Raw sort dictionary if a specific sort is needed.
            populate (bool): Whether to populate referenced documents.
            as_dict (bool): Whether to return documents as dictionaries.
            paginate (bool): Whether to paginate the results.
            current_page (int): The current page number for pagination.
            docs_per_page (int): The number of documents per page.

        Returns:
            ResponsePaginate | list[type[Model]]: Paginated response or list of model instances
                                                  or dictionaries, depending on the 'as_dict' flag.

        Raises:
            TypeError: If the query or sort arguments are not the correct type from pyodmongo.queries.
        """
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
            return await self.__aggregate(
                Model=Model, pipeline=pipeline, as_dict=as_dict, tz_info=tz_info
            )
        max_docs_per_page = 1000
        current_page = 1 if current_page <= 0 else current_page
        docs_per_page = (
            max_docs_per_page if docs_per_page > max_docs_per_page else docs_per_page
        )

        skip = (docs_per_page * current_page) - docs_per_page
        skip_stage = [{"$skip": skip}]
        limit_stage = [{"$limit": docs_per_page}]

        result_pipeline = pipeline + skip_stage + limit_stage

        result, count = await gather(
            self.__aggregate(Model=Model, pipeline=result_pipeline, as_dict=as_dict),
            self.__resolve_count_pipeline(Model=Model, filter_=query),
        )

        page_quantity = ceil(count / docs_per_page)
        return ResponsePaginate(
            current_page=current_page,
            page_quantity=page_quantity,
            docs_quantity=count,
            docs=result,
        )
