from typing import Any, Literal
from .id_model import Id
from datetime import datetime
from typing import TypeVar
from dataclasses import dataclass

from pydantic._internal import (
    _annotated_handlers,
    _config,
    _decorators,
    _fields,
    _forward_ref,
    _generics,
    _mock_val_ser,
    _model_construction,
    _repr,
    _typing_extra,
    _utils,
)

from pydantic._internal._model_construction import *

from pydantic.main import BaseModel

Model = TypeVar('Model', bound='DbModel2')


class DbMeta(type(BaseModel)):
    # def __new__(
    #     mcs,
    #     cls_name: str,
    #     bases: tuple[type[Any], ...],
    #     namespace: dict[str, Any],
    #     __pydantic_generic_metadata__: PydanticGenericMetadata | None = None,
    #     __pydantic_reset_parent_namespace__: bool = True,
    #     **kwargs: Any,
    # ) -> type:
    #     cls: type[Model] = super().__new__(mcs, cls_name, bases, namespace, **kwargs)
    #     return cls
    pass


subclasses = []


class DbModel2(BaseModel):
    id: Id = None
    created_at: datetime = None
    updated_at: datetime = None

    # @classmethod
    # def __init_subclass__(cls):
    #     subclasses.append(cls)

    @classmethod
    def __pydantic_init_subclass__(cls):
        for field in cls.model_fields:
            for field in cls.model_fields:
                setattr(cls, field, 'VALOR SETADO')

    # @classmethod
    # def query(cls, field: str = Literal['id', 'created_at'], value: Any = None):
    #     print('TO NO EQ')

    # @classmethod
    # def init_model(cls):
    #     for field in cls.model_fields:
    #         setattr(cls, field, 'VRAU VALUE INIT')
