from pydantic import ConfigDict
from .id_model import Id
from datetime import datetime
from typing import Any, ClassVar
from ..services.model_init import (
    resolve_indexes,
    resolve_class_fields_db_info,
    resolve_reference_pipeline,
    # resolve_db_fields,
)
from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from typing_extensions import dataclass_transform
from typing import ClassVar
import copy


@dataclass_transform(kw_only_default=True)
class DbMeta(ModelMetaclass):
    """
    Metaclass for database model entities in a PyODMongo environment. It extends
    the functionality of the ModelMetaclass by applying specific behaviors and
    transformations related to database operations such as indexing, reference
    resolution, and initialization of database fields.

    Attributes:
        __pyodmongo_complete__ (bool): Attribute used to track the completion of
                                      the meta-level configuration.

    Methods:
        __new__(cls, name, bases, namespace, **kwargs): Constructs a new class
            instance, ensuring database-specific adjustments and initializations
            are applied.
        __getattr__(cls, name): Custom attribute access handling that supports
            dynamic attributes based on database field definitions.
    """

    def __new__(
        cls, name: str, bases: tuple[Any], namespace: dict, **kwargs: Any
    ) -> type:
        setattr(cls, "__pyodmongo_complete__", False)
        for base in bases:
            setattr(base, "__pyodmongo_complete__", False)

        # TODO finish db_fields after ModelMetaclass
        # db_fields = copy.deepcopy(namespace.get("__annotations__"))
        # db_fields = resolve_db_fields(bases=bases, db_fields=db_fields)

        cls: BaseModel = ModelMetaclass.__new__(cls, name, bases, namespace, **kwargs)

        setattr(cls, "__pyodmongo_complete__", True)
        for base in bases:
            setattr(base, "__pyodmongo_complete__", True)

        resolve_class_fields_db_info(cls=cls)
        pipeline = resolve_reference_pipeline(cls=cls, pipeline=[])
        setattr(cls, "_reference_pipeline", pipeline)
        indexes = resolve_indexes(cls=cls)
        setattr(cls, "_init_indexes", indexes)
        return cls

    def __getattr__(cls, name: str):
        if cls.__dict__.get("__pyodmongo_complete__"):
            is_attr = name in cls.__dict__.get("model_fields").keys()
            if is_attr:
                return cls.__dict__.get(name + "__pyodmongo")
        ModelMetaclass.__getattr__(cls, name)


class DbModel(BaseModel, metaclass=DbMeta):
    """
    Base class for all database models using PyODMongo with auto-mapped fields
    to MongoDB documents. Provides automatic timestamping and ID management,
    along with utilities for managing nested dictionary fields.

    Attributes:
        id (Id | None): Unique identifier for the database record, typically
                        mapped to MongoDB's '_id'.
        created_at (datetime | None): Timestamp indicating when the record was
                                      created.
        updated_at (datetime | None): Timestamp indicating when the record was
                                      last updated.
        model_config (ConfigDict): Configuration dictionary to control model
                                   serialization and deserialization behaviors.
        _pipeline (ClassVar): Class variable to store pipeline operations for
                              reference resolution.

    Methods:
        __init__(**attrs): Initializes a new instance of DbModel, applying
                           transformations to nested dictionary fields to clean
                           up empty values.
        __remove_empty_dict(dct): Recursively removes empty dictionaries from
                                  nested dictionary fields, aiding in the
                                  cleanup process during initialization.
    """

    id: Id | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(populate_by_name=True)
    _pipeline: ClassVar = []

    def __remove_empty_dict(self, dct: dict):
        if dct == {}:
            return None
        for key, value in dct.items():
            if value == {}:
                dct[key] = None
            elif type(value) == dict:
                dct[key] = self.__remove_empty_dict(dct=value)
        is_full_empty = all(v == None or v == {} for v in dct.values())
        if is_full_empty:
            return None
        return dct

    def __init__(self, **attrs):
        for key, value in attrs.items():
            if type(value) == dict:
                attrs[key] = self.__remove_empty_dict(dct=value)
        if attrs.get("_id") is not None:
            attrs["id"] = attrs.pop("_id")
        super().__init__(**attrs)
