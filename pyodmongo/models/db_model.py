from pydantic import ConfigDict
from .id_model import Id
from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel
from typing import ClassVar
from .metaclasses import PyOdmongoMeta, DbMeta
from pydantic_core import PydanticUndefined


class MainBaseModel(BaseModel, metaclass=PyOdmongoMeta):
    """
    Base class for all models in PyODMongo, using PyOdmongoMeta as its metaclass.
    This class provides the foundational structure for other models, enabling
    the integration of database-specific configurations and behaviors.

    Attributes:
        None (The class itself does not define any attributes; it serves as a
              base for other models to extend and utilize the provided metaclass.)

    Methods:
        None (The class does not define any methods; it relies on the metaclass
              and derived classes for functionality.)
    """


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
    _default_language: ClassVar = None

    def __replace_empty_dicts(self, data):
        """
        Recursively traverses a dictionary (or a list of dictionaries) and:
        - Replaces empty dictionaries with None.
        - Removes empty dictionaries from lists.

        Args:
            data (dict | list): The dictionary or list to process.

        Returns:
            dict | list: The processed dictionary or list with modifications.
        """

        if isinstance(data, dict):
            if "_id" in data:
                data["id"] = data.pop("_id")
            for key, value in data.items():
                if isinstance(value, dict):
                    if not value:
                        data[key] = None
                    else:
                        self.__replace_empty_dicts(value)
                elif isinstance(value, list):
                    data[key] = [
                        (
                            self.__replace_empty_dicts(item)
                            if isinstance(item, dict)
                            else item
                        )
                        for item in value
                        if not (isinstance(item, dict) and not item)
                    ]
        return data

    def __init__(self, **attrs):
        self.__replace_empty_dicts(attrs)
        super().__init__(**attrs)
