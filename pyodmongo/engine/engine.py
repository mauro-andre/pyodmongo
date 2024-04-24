from pymongo import MongoClient
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


Model = TypeVar("Model", bound=DbModel)


class DbEngine:
    """
    Handles synchronous database operations using MongoDB with the MongoClient.
    This class provides methods for CRUD operations, supporting complex queries,
    aggregations, and directly interacting with MongoDB collections in a synchronous manner.

    Methods:
        __init__(mongo_uri, db_name): Initializes the MongoClient with the provided MongoDB URI and selects the database by name.
        __save_dict(obj, dict_to_save, collection, indexes, query): Private method to save or update documents in the specified collection.
        __aggregate(Model, pipeline, as_dict): Private method to perform aggregation queries.
        __resolve_count_pipeline(Model, filter_): Private method to count documents based on a filter.
        delete_one(Model, query, raw_query): Deletes a single document based on the provided query.
        delete(Model, query, raw_query): Deletes multiple documents based on the provided query.
        save(obj, query, raw_query): Saves or updates a document in the database.
        save_all(obj_list): Saves multiple documents.
        find_one(Model, query, raw_query, sort, raw_sort, populate, as_dict): Finds a single document.
        find_many(Model, query, raw_query, sort, raw_sort, populate, as_dict, paginate, current_page, docs_per_page): Finds multiple documents with optional pagination.
    """

    def __init__(self, mongo_uri, db_name, tz_info: timezone = None):
        """
        Initializes the database engine with a MongoDB connection URI and database name.
        Sets up the client and selects the specified database.

        Args:
            mongo_uri (str): MongoDB URI to connect to.
            db_name (str): Name of the database to operate on.
        """
        self._client = MongoClient(mongo_uri)
        self._db = self._client[db_name]
        self._tz_info = tz_info

    # ----------DB OPERATIONS----------
    def __save_dict(
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
        """
        Synchronously deletes a single document from the database based on the specified
        query or raw_query.

        Args:
            Model (type[Model]): The model class that defines the MongoDB collection.
            query (ComparisonOperator | LogicalOperator, optional): The structured query object.
            raw_query (dict, optional): Raw MongoDB query dictionary if a specific condition is needed.

        Returns:
            DeleteResponse: A response object containing details of the delete operation.

        Raises:
            TypeError: If the query argument is not of type ComparisonOperator or LogicalOperator.
        """
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
        """
        Synchronously deletes multiple documents from the database based on the specified
        query or raw_query. This method handles the deletion operation through a structured
        query or a directly provided MongoDB query dictionary, offering flexibility in how
        deletions are specified.

        Args:
            Model (type[Model]): The model class that defines the MongoDB collection to operate on.
            query (ComparisonOperator | LogicalOperator, optional): The structured query object to
                filter documents to be deleted. Must be an instance of ComparisonOperator or LogicalOperator.
            raw_query (dict, optional): Raw MongoDB query dictionary if a more specific or complex
                condition is required than what is provided by the structured query.

        Returns:
            DeleteResponse: A response object containing details of the delete operation, including
                            whether the operation was acknowledged by the MongoDB server, how many
                            documents were deleted, and the raw result from the MongoDB operation.

        Raises:
            TypeError: If the `query` argument is provided but is not of type ComparisonOperator or
                       LogicalOperator, ensuring only valid query types are used for database operations.
        """
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
        """
        Synchronously saves or updates a document in the database. This method handles the
        preparation and execution of a save or update operation based on a structured query
        or a raw MongoDB query. It utilizes specified indexes and handles the timing for
        created and updated timestamps.

        Args:
            obj (type[Model]): The model instance to be saved or updated. The model should
                define `_indexes`, `updated_at`, and `created_at` field specifications.
            query (ComparisonOperator | LogicalOperator, optional): The query used to locate
                the document for update operations. It must be either a ComparisonOperator or
                LogicalOperator to validate document matching.
            raw_query (dict, optional): A raw MongoDB query dictionary if specific conditions
                are needed that cannot be expressed using the structured query objects.

        Returns:
            SaveResponse: An object detailing the outcome of the save operation, including
                          acknowledgment status, counts of matched and modified documents,
                          the ID of any upserted document, and the raw MongoDB operation result.

        Raises:
            TypeError: If the `query` argument is provided but is not of the correct types,
                       ensuring that the operation only proceeds with valid query parameters.
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
        """
        Synchronously saves a list of model instances to the database. This method iterates through
        each model instance in the provided list, saving each using the save method, and collects the
        responses.

        Args:
            obj_list (list): A list of model instances to be saved to the database.

        Returns:
            list[SaveResponse]: A list of SaveResponse objects detailing the outcomes of the save
                                operations for each model instance.

        Notes:
            This method calls the save method for each object in the list, which means it may not
            be the most efficient way to save multiple objects due to the lack of bulk operation optimizations.
        """
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
        tz_info: timezone = None,
    ) -> type[Model]:
        """
        Synchronously finds a single document in the database that matches the specified
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
            type[Model] | None: The found document as a model instance or dictionary, or None if no document matches the query.

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
            result = self.__aggregate(
                Model=Model, pipeline=pipeline, as_dict=as_dict, tz_info=tz_info
            )
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
        tz_info: timezone = None,
        paginate: bool = False,
        current_page: int = 1,
        docs_per_page: int = 1000,
    ):
        """
        Synchronously retrieves multiple documents from the database based on the specified
        query conditions, supports sorting, and optionally returns paginated results.

        Args:
            Model (type[Model]): The model class defining the structure of the documents.
            query (ComparisonOperator | LogicalOperator, optional): The structured query object to filter documents.
            raw_query (dict, optional): Raw MongoDB query dictionary if specific conditions are needed.
            sort (SortOperator, optional): Sorting instructions for the results.
            raw_sort (dict, optional): Raw sort dictionary if a specific sort is needed.
            populate (bool): Whether to populate referenced documents.
            as_dict (bool): Whether to return the documents as dictionaries.
            paginate (bool): Whether to paginate the results.
            current_page (int): The current page number for pagination.
            docs_per_page (int): The number of documents per page.

        Returns:
            list[type[Model]] | ResponsePaginate: A list of model instances or dictionaries, or a
                                                  paginated response object if pagination is enabled.

        Raises:
            TypeError: If the query or sort arguments are not the correct type from pyodmongo.queries.
            IndexError: If no documents are found and a single document is expected to be returned.

        Notes:
            The method constructs a MongoDB aggregation pipeline based on the query and sort parameters.
            If pagination is enabled, the method calculates the total number of pages and configures
            the pagination stages in the pipeline accordingly.
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
            return self.__aggregate(
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
