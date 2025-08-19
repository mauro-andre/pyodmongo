from pydantic import BaseModel
from bson import ObjectId
from ..models.id_model import Id
from ..models.db_model import MainBaseModel
from ..models.db_field_info import DbField
from ..models.db_decimal import DbDecimal
from ..services.reference_pipeline import resolve_reference_pipeline
from ..services.verify_subclasses import is_subclass
from decimal import Decimal
from bson import Decimal128


def consolidate_dict(obj: MainBaseModel, dct: dict, populate: bool):
    """
    Recursively consolidates the attributes of a Pydantic model into a dictionary,
    handling nested models, list fields, and references appropriately based on the model's
    field specifications.

    Args:
        obj (MainBaseModel): The PyODMongo model instance from which to extract data.
        dct (dict): The dictionary into which data should be consolidated. This dictionary
                    is modified in-place.

    Returns:
        dict: The modified dictionary with model data consolidated into it, including handling
              of MongoDB ObjectId conversions and nested structures.

    Description:
        This function iterates over each field of the provided model instance, extracting the
        value and associated metadata. Depending on whether the field contains model data,
        is a list, or is a reference, the function appropriately processes the value to fit
        MongoDB storage requirements, including converting to ObjectIds where necessary.
        The function is recursive for nested models and lists of models.
    """
    for field, field_info in obj.__class__.model_fields.items():
        value = getattr(obj, field)
        try:
            db_field_info: DbField = getattr(obj.__class__, field)
        except AttributeError:
            if is_subclass(class_to_verify=obj.__class__, subclass=BaseModel):
                raise TypeError(
                    f"The {obj.__class__.__name__} class inherits from Pydantic's BaseModel class. Try switching to PyODMongo's MainBaseModel class"
                )
        alias = db_field_info.field_alias
        has_model_fields = db_field_info.has_model_fields
        is_list = db_field_info.is_list
        by_reference = db_field_info.by_reference and not populate
        if has_model_fields:
            if value is None:
                dct[alias] = None
                continue
            if not is_list:
                if by_reference:
                    try:
                        dct[alias] = ObjectId(value.id)
                    except AttributeError:
                        dct[alias] = ObjectId(value)
                else:
                    dct[alias] = {}
                    consolidate_dict(obj=value, dct=dct[alias], populate=populate)
            else:
                if by_reference:
                    try:
                        dct[alias] = [ObjectId(o.id) for o in value]
                    except AttributeError:
                        dct[alias] = [ObjectId(o) for o in value]
                else:
                    dct[alias] = []
                    for v in value:
                        obj_lst_elem = {}
                        consolidate_dict(obj=v, dct=obj_lst_elem, populate=populate)
                        dct[alias].append(obj_lst_elem)
        else:
            if db_field_info.field_type == Id and value is not None:
                if is_list:
                    dct[alias] = [ObjectId(o) for o in value if ObjectId.is_valid(o)]
                else:
                    dct[alias] = ObjectId(value) if ObjectId.is_valid(value) else value
            elif (
                db_field_info.field_type == Decimal
                or db_field_info.field_type == DbDecimal
            ) and value is not None:
                if is_list:
                    dct[alias] = [Decimal128(str(o)) for o in value]
                else:
                    dct[alias] = Decimal128(str(value))
            else:
                dct[alias] = value
    return dct


def _skip_and_limit_stages(current_page: int, docs_per_page: int):
    """
    Add pagination stages to the aggregation pipeline.

    Args:
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
    return skip_stage, limit_stage


def mount_base_pipeline(
    Model,
    query: dict,
    sort: dict,
    populate: bool,
    pipeline: list | None,
    populate_db_fields: list[DbField] | None,
    paginate: int,
    current_page: int,
    docs_per_page: int,
    no_paginate_limit: int | None,
):
    """
    Mounts a base MongoDB aggregation pipeline for find operations.

    This function constructs a pipeline by combining various stages, such as
    document matching, sorting, reference population, and pagination,
    based on the provided parameters. It serves as the core pipeline
    builder for find queries.

    Args:
        Model: The PyODMongo model class for the query.
        query: The MongoDB query dictionary for the `$match` stage.
        sort: The dictionary defining the sort order for the `$sort` stage.
        populate: If True, adds stages to populate referenced documents.
        pipeline: An optional list of aggregation stages to prepend to the
                  pipeline. If None, the model's default `_pipeline` is used.
        populate_db_fields: A list of specific `DbField`s to populate.
                            Used only if `populate` is True.
        paginate: If True, enables pagination by adding `$skip` and `$limit`
                  stages.
        current_page: The page number to retrieve when pagination is enabled.
        docs_per_page: The number of documents per page for pagination.
        no_paginate_limit: The maximum number of documents to return when
                           pagination is disabled.
        is_find_one: If True, adds a `$limit: 1` stage to the pipeline,
                     optimizing the query for a single document.

    Returns:
        A list representing the complete MongoDB aggregation pipeline.
    """
    match_stage = [{"$match": query}]
    sort_stage = [{"$sort": sort}] if sort != {} else []
    skip_stage = []
    limit_stage = [{"$limit": no_paginate_limit}] if no_paginate_limit else []
    pipeline = pipeline or Model._pipeline
    if paginate:
        skip_stage, limit_stage = _skip_and_limit_stages(
            current_page=current_page, docs_per_page=docs_per_page
        )
    if pipeline:
        return match_stage + pipeline + sort_stage + skip_stage + limit_stage
    if populate:
        reference_stage = resolve_reference_pipeline(
            cls=Model, pipeline=[], populate_db_fields=populate_db_fields
        )
        return match_stage + reference_stage + sort_stage + skip_stage + limit_stage
    else:
        return match_stage + sort_stage + skip_stage + limit_stage
