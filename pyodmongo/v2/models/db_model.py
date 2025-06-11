from ..metaclasses.main_meta import MainMeta

from .db_field import DbField
from .id_model import Id
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from bson import ObjectId, Decimal128
from decimal import Decimal
from typing import Any


class MainBaseModel(BaseModel, metaclass=MainMeta):
    def model_dump_db(self) -> dict:
        db_fields: list[DbField] = [
            v for k, v in self.__class__.__dict__.items() if isinstance(v, DbField)
        ]

        def recursive(db_field: DbField, value: Any) -> dict:
            # IF VALUE IS DBMODEL OR MAINBASEMODEL AND NOR REFERENCE
            if isinstance(value, MainBaseModel) and not db_field.by_reference:
                value = value.model_dump_db()

            # IF IS REFERENCE OR ID FIELD
            elif db_field.field_alias == "_id" or (
                db_field.by_reference and not db_field.is_list
            ):
                try:
                    value = ObjectId(value)
                except TypeError:
                    value = ObjectId(value.id)

            # IF IS A LIST
            elif db_field.is_list:
                # OF REFERENCES
                if db_field.by_reference:
                    value = [
                        ObjectId(v.id) if hasattr(v, "id") else ObjectId(v)
                        for v in value
                    ]
                else:
                    value = [recursive(db_field=db_field, value=v)[1] for v in value]

            # IF VALUE IS DECIMAL
            elif isinstance(value, Decimal):
                value = Decimal128(value)

            elif isinstance(value, str) or isinstance(value, Id):
                try:
                    value = ObjectId(value)
                except Exception:
                    value = value

            return db_field.field_alias, value

        return {
            key: value
            for db_field in db_fields
            for key, value in [
                recursive(db_field=db_field, value=getattr(self, db_field.field_name))
            ]
        }


class DbModel(MainBaseModel):
    id: Id | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    _collection: str
    model_config = ConfigDict(populate_by_name=True)
