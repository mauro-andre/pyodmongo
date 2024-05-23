from pyodmongo import MainBaseModel, DbModel, Id
from pyodmongo.models.db_field_info import DbField
from pydantic import EmailStr, ValidationError
from datetime import datetime
from typing import ClassVar, Union
import pytest


def test_main_base_model():
    class MainModel(MainBaseModel):
        attr_1: int
        attr_2: str
        attr_3: Id | None

    assert issubclass(MainModel, MainBaseModel)
    assert isinstance(MainModel.attr_1, DbField)
    assert isinstance(MainModel.attr_2, DbField)
    obj = MainModel(attr_1=1, attr_2="one", attr_3=None)
    assert obj.attr_1 == 1
    assert obj.attr_2 == "one"


def test_create_class():
    class MyClass(DbModel):
        _collection: ClassVar = "myclass"

    assert issubclass(MyClass, DbModel)


def test_class_variable_db_model():
    class MyClass(DbModel):
        _collection: ClassVar = "myclass"

    assert hasattr(MyClass, "id")
    assert hasattr(MyClass, "created_at")
    assert hasattr(MyClass, "updated_at")


def test_dbmodel_class_variables_type_annotation():
    class MyClass(DbModel):
        _collection: ClassVar = "myclass"

    assert MyClass.model_fields["id"].annotation == Union[Id, None]
    assert MyClass.model_fields["created_at"].annotation == Union[datetime, None]
    assert MyClass.model_fields["updated_at"].annotation == Union[datetime, None]


def test_class_inheritance():
    class MyClassMain(DbModel):
        attr_main: str
        _collection: ClassVar = "myclassmain"

    class MyClass1(MyClassMain):
        attr_1: str
        _collection: ClassVar = "myclass1"

    class MyClass1_1(MyClass1):
        attr_1_1: str
        _collection: ClassVar = "myclass1_2"

    class MyClass2(MyClassMain):
        attr_2: str
        _collection: ClassVar = "myclass2"

    class MyClass2_2(MyClass2):
        attr_2_2: str
        _collection: ClassVar = "myclass2_2"

    assert hasattr(MyClassMain, "attr_main")
    assert not hasattr(MyClassMain, "attr_1")
    assert not hasattr(MyClassMain, "attr_1_1")
    assert not hasattr(MyClassMain, "attr_2")
    assert not hasattr(MyClassMain, "attr_2_2")
    assert hasattr(MyClass1, "attr_main")
    assert hasattr(MyClass1, "attr_1")
    assert not hasattr(MyClass1, "attr_1_1")
    assert not hasattr(MyClass1, "attr_2")
    assert not hasattr(MyClass1, "attr_2_2")
    assert hasattr(MyClass1_1, "attr_main")
    assert hasattr(MyClass1_1, "attr_1")
    assert hasattr(MyClass1_1, "attr_1_1")
    assert not hasattr(MyClass1_1, "attr_2")
    assert not hasattr(MyClass1_1, "attr_2_2")
    assert hasattr(MyClass2, "attr_main")
    assert not hasattr(MyClass2, "attr_1")
    assert not hasattr(MyClass2, "attr_1_1")
    assert hasattr(MyClass2, "attr_2")
    assert not hasattr(MyClass2, "attr_2_2")
    assert hasattr(MyClass2_2, "attr_main")
    assert not hasattr(MyClass2_2, "attr_1")
    assert not hasattr(MyClass2_2, "attr_1_1")
    assert hasattr(MyClass2_2, "attr_2")
    assert hasattr(MyClass2_2, "attr_2_2")
    assert hasattr(MyClassMain, "id")
    assert hasattr(MyClassMain, "created_at")
    assert hasattr(MyClassMain, "updated_at")
    assert hasattr(MyClass1, "id")
    assert hasattr(MyClass1, "created_at")
    assert hasattr(MyClass1, "updated_at")
    assert hasattr(MyClass1_1, "id")
    assert hasattr(MyClass1_1, "created_at")
    assert hasattr(MyClass1_1, "updated_at")
    assert hasattr(MyClass2, "id")
    assert hasattr(MyClass2, "created_at")
    assert hasattr(MyClass2, "updated_at")
    assert hasattr(MyClass2_2, "id")
    assert hasattr(MyClass2_2, "created_at")
    assert hasattr(MyClass2_2, "updated_at")


def test_fields_inheritance():
    class MyClassMain(DbModel):
        attr_main: str
        _collection: ClassVar = "myclassmain"

    class MyClass1(MyClassMain):
        attr_1: str
        _collection: ClassVar = "myclass1"

    class MyClass1_1(MyClass1):
        attr_1_1: str
        _collection: ClassVar = "myclass1_2"

    class MyClass2(MyClassMain):
        attr_2: str
        _collection: ClassVar = "myclass2"

    class MyClass2_2(MyClass2):
        attr_2_2: str
        _collection: ClassVar = "myclass2_2"

    assert "id" in MyClassMain.model_fields
    assert "created_at" in MyClassMain.model_fields
    assert "updated_at" in MyClassMain.model_fields
    assert "attr_main" in MyClassMain.model_fields
    assert "attr_1" not in MyClassMain.model_fields
    assert "attr_1_1" not in MyClassMain.model_fields
    assert "attr_2" not in MyClassMain.model_fields
    assert "attr_2_2" not in MyClassMain.model_fields

    assert "id" in MyClass1.model_fields
    assert "created_at" in MyClass1.model_fields
    assert "updated_at" in MyClass1.model_fields
    assert "attr_main" in MyClass1.model_fields
    assert "attr_1" in MyClass1.model_fields
    assert "attr_1_1" not in MyClass1.model_fields
    assert "attr_2" not in MyClass1.model_fields
    assert "attr_2_2" not in MyClass1.model_fields

    assert "id" in MyClass1_1.model_fields
    assert "created_at" in MyClass1_1.model_fields
    assert "updated_at" in MyClass1_1.model_fields
    assert "attr_main" in MyClass1_1.model_fields
    assert "attr_1" in MyClass1_1.model_fields
    assert "attr_1_1" in MyClass1_1.model_fields
    assert "attr_2" not in MyClass1_1.model_fields
    assert "attr_2_2" not in MyClass1_1.model_fields

    assert "id" in MyClass2.model_fields
    assert "created_at" in MyClass2.model_fields
    assert "updated_at" in MyClass2.model_fields
    assert "attr_main" in MyClass2.model_fields
    assert "attr_1" not in MyClass2.model_fields
    assert "attr_1_1" not in MyClass2.model_fields
    assert "attr_2" in MyClass2.model_fields
    assert "attr_2_2" not in MyClass2.model_fields

    assert "id" in MyClass2_2.model_fields
    assert "created_at" in MyClass2_2.model_fields
    assert "updated_at" in MyClass2_2.model_fields
    assert "attr_main" in MyClass2_2.model_fields
    assert "attr_1" not in MyClass2_2.model_fields
    assert "attr_1_1" not in MyClass2_2.model_fields
    assert "attr_2" in MyClass2_2.model_fields
    assert "attr_2_2" in MyClass2_2.model_fields


def test_field_with_email_str():
    class MyClass(DbModel):
        attr_1: str
        email: EmailStr

    with pytest.raises(ValidationError):
        obj = MyClass(attr_1="Value one", email="shunda")


def test_polymorphism():
    class FirstClass(DbModel):
        attr_1: str = "one"
        attr_2: int = 2

    class SecondClass(FirstClass):
        attr_1: int = 1
        attr_3: int = 3

    obj_1 = FirstClass()
    obj_2 = SecondClass()

    assert obj_1.attr_1 == "one"
    assert type(obj_1.attr_1) is str
    assert obj_2.attr_1 == 1
    assert type(obj_2.attr_1) is int
