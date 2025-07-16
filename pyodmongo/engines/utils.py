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
    is_find_one: bool,
):
    """
    Constructs a basic MongoDB aggregation pipeline based on the provided query, sort, and
    model settings, optionally including reference population stages.

    Args:
        Model (type[Model]): The model class defining the MongoDB collection and its aggregation logic.
        query (dict): MongoDB query dictionary to filter the documents.
        sort (dict): Dictionary defining the sorting order of the documents.
        populate (bool): Flag indicating whether to include reference population stages in the pipeline.

    Returns:
        list: The MongoDB aggregation pipeline configured with match, sort, and optionally population stages.

    Description:
        This function constructs a MongoDB aggregation pipeline using the provided model's
        internal pipeline stages and the specified query and sort parameters. If 'populate' is
        true, reference population stages defined in the model are included to resolve document
        references as part of the aggregation process.
    """
    match_stage = [{"$match": query}]
    sort_stage = [{"$sort": sort}] if sort != {} else []
    skip_stage = []
    limit_stage = [{"$limit": 1}] if is_find_one else []
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
