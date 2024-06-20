from typing import Any
from ..services.model_init import (
    resolve_indexes,
    resolve_class_fields_db_info,
)
from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from typing_extensions import dataclass_transform


@dataclass_transform(kw_only_default=True)
class PyOdmongoMeta(ModelMetaclass):
    """
    Metaclass for creating and configuring PyODMongo models. This metaclass extends
    the functionality of Pydantic's ModelMetaclass to include database-specific
    configurations and transformations.

    The primary responsibilities of this metaclass are:
    - Setting and tracking the `__pyodmongo_complete__` attribute to ensure proper
      initialization of database-related features.
    - Applying necessary transformations to class fields for database compatibility.
    - Providing custom attribute access behavior for dynamically generated attributes.

    Attributes:
        __pyodmongo_complete__ (bool): Indicator of whether the meta-level
                                       configuration is complete.

    Methods:
        __new__(cls, name, bases, namespace, **kwargs): Constructs a new class instance,
            applying database-specific initializations.
        __getattr__(cls, name): Custom attribute access method supporting dynamic
            attribute retrieval based on model fields.
    """

    def __new__(
        cls, name: str, bases: tuple[Any], namespace: dict, **kwargs: Any
    ) -> type:
        setattr(cls, "__pyodmongo_complete__", False)
        for base in bases:
            setattr(base, "__pyodmongo_complete__", False)

        cls: BaseModel = ModelMetaclass.__new__(cls, name, bases, namespace, **kwargs)

        setattr(cls, "__pyodmongo_complete__", True)
        for base in bases:
            setattr(base, "__pyodmongo_complete__", True)

        resolve_class_fields_db_info(cls=cls)
        return cls

    def __getattr__(cls, name: str):
        if cls.__dict__.get("__pyodmongo_complete__"):
            is_attr = name in cls.__dict__.get("model_fields").keys()
            if is_attr:
                return cls.__dict__.get(name + "__pyodmongo")
        ModelMetaclass.__getattr__(cls, name)


@dataclass_transform(kw_only_default=True)
class DbMeta(PyOdmongoMeta):
    """
    Metaclass for database model entities in a PyODMongo environment. It extends
    the functionality of the PyOdmongoMeta by applying specific behaviors and
    transformations related to database operations such as indexing, reference
    resolution, and initialization of database fields.

    The primary responsibilities of this metaclass are:
    - Constructing new class instances with additional database-specific adjustments
      and initializations.
    - Setting up pipelines for resolving references within the database context.
    - Configuring indexes for efficient database operations.

    Attributes:
        __pyodmongo_complete__ (bool): Attribute used to track the completion of
                                       the meta-level configuration.

    Methods:
        __new__(cls, name, bases, namespace, **kwargs): Constructs a new class instance,
            ensuring database-specific adjustments and initializations are applied.
    """

    def __new__(
        cls, name: str, bases: tuple[Any], namespace: dict, **kwargs: Any
    ) -> type:
        cls: BaseModel = PyOdmongoMeta.__new__(cls, name, bases, namespace, **kwargs)

        indexes = resolve_indexes(cls=cls)
        setattr(cls, "_init_indexes", indexes)
        return cls
