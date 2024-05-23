from pydantic import ConfigDict
from .id_model import Id
from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel
from typing import ClassVar
from .metaclasses import PyOdmongoMeta, DbMeta


class MainBaseModel(BaseModel, metaclass=PyOdmongoMeta): ...


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
