from pyodmongo import DbModel, Id
from typing import ClassVar
from pydantic import BaseModel
from pyodmongo.services.model_init import field_annotation_infos


def test_field_with_list_of_unions():
    class MyFirstClass(BaseModel):
        attr_first: str = None
        _collection: ClassVar = 'my_first_class'

    class MyClass(BaseModel):
        email: str = None
        mfc0: Id = None
        mfc1: list[MyFirstClass | None | Id] | None = None

    for field, field_info in MyClass.model_fields.items():
        db_field_info = field_annotation_infos(field=field, field_info=field_info)
