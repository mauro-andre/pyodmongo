from pyodmongo.v2 import DbModel, MainBaseModel, Id, Field
from pyodmongo.v2.engines.utils import consolidate_dict
from typing import ClassVar
from datetime import datetime
from bson import ObjectId, Decimal128
from decimal import Decimal


def test_dict_to_save():
    class MainBaseModel1(MainBaseModel):
        field1: str
        field2: int

    class MainBaseModel2(MainBaseModel):
        field1: str
        model_1: MainBaseModel1

    class DbModel1(DbModel):
        field1: str
        field2: str = Field(default="Default value", alias="field2Alias")
        model_2: MainBaseModel2
        _collection: ClassVar = "db_model_1"

    class DbModel2(DbModel):
        field1: str
        field2: str = Field(default="Default value", alias="field2Alias")
        field3: DbModel1
        field4: DbModel1 | Id
        field5: list[DbModel1]
        field6: list[DbModel1 | Id]
        _collection: ClassVar = "db_model_2"

    # Create auxiliary objects for the tests
    obj_main_base_model_1_a = MainBaseModel1(field1="mbm1a", field2=1)
    obj_main_base_model_1_b = MainBaseModel1(field1="mbm1b", field2=2)
    obj_main_base_model_1_c = MainBaseModel1(field1="mbm1c", field2=3)

    obj_main_base_model_2_a = MainBaseModel2(
        field1="mbm2a", model_1=obj_main_base_model_1_a
    )
    obj_main_base_model_2_b = MainBaseModel2(
        field1="mbm2b", model_1=obj_main_base_model_1_b
    )
    obj_main_base_model_2_c = MainBaseModel2(
        field1="mbm2c", model_1=obj_main_base_model_1_c
    )

    # Create ObjectIds for DbModel1 instances
    obj_db_model_1_1_id = ObjectId()
    obj_db_model_1_2_id = ObjectId()
    obj_db_model_1_3_id = ObjectId()
    obj_db_model_1_4_id = ObjectId()

    # Create DbModel1 objects
    obj_db_model_1_1 = DbModel1(
        id=obj_db_model_1_1_id, field1="dbm1-1", model_2=obj_main_base_model_2_a
    )
    obj_db_model_1_2 = DbModel1(
        id=obj_db_model_1_2_id, field1="dbm1-2", model_2=obj_main_base_model_2_b
    )
    obj_db_model_1_3 = DbModel1(
        id=obj_db_model_1_3_id, field1="dbm1-3", model_2=obj_main_base_model_2_c
    )
    obj_db_model_1_4 = DbModel1(
        id=obj_db_model_1_4_id, field1="dbm1-4", model_2=obj_main_base_model_2_a
    )

    # Create ObjectIds for DbModel2 instances
    obj_db_model_2_1_id = ObjectId()
    obj_db_model_2_2_id = ObjectId()

    # DbModel2 exemplo 1: field3 = DbModel1, field4 = DbModel1, field5 = lista de objetos, field6 = lista de objetos
    obj_db_model_2_1 = DbModel2(
        id=obj_db_model_2_1_id,
        field1="dbm2-1",
        field3=obj_db_model_1_1,
        field4=obj_db_model_1_2,
        field5=[obj_db_model_1_3, obj_db_model_1_4],
        field6=[obj_db_model_1_4],
    )

    # DbModel2 exemplo 2: field3 = DbModel1, field4 = Id, field5 = lista de objetos, field6 = lista de Ids
    obj_db_model_2_2 = DbModel2(
        id=obj_db_model_2_2_id,
        field1="dbm2-2",
        field3=obj_db_model_1_2,
        field4=obj_db_model_1_1_id,
        field5=[obj_db_model_1_3, obj_db_model_1_4],
        field6=[obj_db_model_1_2_id, obj_db_model_1_3_id],
    )
    # obj_db_model_2_1_dict = obj_db_model_2_1.model_dump_db()
    assert obj_db_model_2_1.model_dump_db() == {
        "_id": obj_db_model_2_1_id,
        "created_at": None,
        "updated_at": None,
        "field1": "dbm2-1",
        "field2Alias": "Default value",
        "field3": {
            "_id": obj_db_model_1_1_id,
            "created_at": None,
            "updated_at": None,
            "field1": "dbm1-1",
            "field2Alias": "Default value",
            "model_2": {"field1": "mbm2a", "model_1": {"field1": "mbm1a", "field2": 1}},
        },
        "field4": obj_db_model_1_2_id,
        "field5": [
            {
                "_id": obj_db_model_1_3_id,
                "created_at": None,
                "updated_at": None,
                "field1": "dbm1-3",
                "field2Alias": "Default value",
                "model_2": {
                    "field1": "mbm2c",
                    "model_1": {"field1": "mbm1c", "field2": 3},
                },
            },
            {
                "_id": obj_db_model_1_4_id,
                "created_at": None,
                "updated_at": None,
                "field1": "dbm1-4",
                "field2Alias": "Default value",
                "model_2": {
                    "field1": "mbm2a",
                    "model_1": {"field1": "mbm1a", "field2": 1},
                },
            },
        ],
        "field6": [obj_db_model_1_4_id],
    }

    obj_db_model_2_2.model_dump_db() == {
        "_id": obj_db_model_2_2_id,
        "created_at": None,
        "updated_at": None,
        "field1": "dbm2-2",
        "field2Alias": "Default value",
        "field3": {
            "_id": obj_db_model_1_2_id,
            "created_at": None,
            "updated_at": None,
            "field1": "dbm1-2",
            "field2Alias": "Default value",
            "model_2": {"field1": "mbm2b", "model_1": {"field1": "mbm1b", "field2": 2}},
        },
        "field4": obj_db_model_1_1_id,
        "field5": [
            {
                "_id": obj_db_model_1_3_id,
                "created_at": None,
                "updated_at": None,
                "field1": "dbm1-3",
                "field2Alias": "Default value",
                "model_2": {
                    "field1": "mbm2c",
                    "model_1": {"field1": "mbm1c", "field2": 3},
                },
            },
            {
                "_id": obj_db_model_1_4_id,
                "created_at": None,
                "updated_at": None,
                "field1": "dbm1-4",
                "field2Alias": "Default value",
                "model_2": {
                    "field1": "mbm2a",
                    "model_1": {"field1": "mbm1a", "field2": 1},
                },
            },
        ],
        "field6": [obj_db_model_1_2_id, obj_db_model_1_3_id],
    }


def test_model_dump_db_reference_and_list_reference_union():
    class RefModel(DbModel):
        field_a: str
        _collection: ClassVar = "ref"

    class ModelWithUnionRef(DbModel):
        ref1: RefModel | Id
        ref_list: list[RefModel | Id]
        _collection: ClassVar = "union"

    oid1 = ObjectId()
    oid2 = ObjectId()
    obj_ref1 = RefModel(id=oid1, field_a="x")
    obj_ref2 = RefModel(id=oid2, field_a="y")

    # Quando o valor é o modelo, deve serializar só o ObjectId
    obj = ModelWithUnionRef(ref1=obj_ref1, ref_list=[obj_ref1, oid2])
    result = obj.model_dump_db()
    assert result["ref1"] == oid1
    assert result["ref_list"] == [oid1, oid2]


def test_model_dump_db_only_model():
    class SimpleChild(MainBaseModel):
        x: int

    class ParentModel(MainBaseModel):
        child: SimpleChild

    obj = ParentModel(child=SimpleChild(x=35))
    result = obj.model_dump_db()
    assert result["child"] == {"x": 35}


def test_model_dump_db_decimal_type():
    class DecModel(MainBaseModel):
        price: Decimal

    obj = DecModel(price=Decimal("123.45"))
    result = obj.model_dump_db()
    assert isinstance(result["price"], Decimal128)
    assert result["price"].to_decimal() == Decimal("123.45")


def test_model_dump_db_primitives_and_fallback_string():
    class StrModel(MainBaseModel):
        s: str
        i: int
        f: float

    oid = ObjectId()
    obj = StrModel(s=str(oid), i=10, f=20.5)
    result = obj.model_dump_db()
    assert result["s"] == oid
    assert result["i"] == 10
    assert result["f"] == 20.5

    obj2 = StrModel(s="nao_e_oid", i=0, f=1.5)
    result2 = obj2.model_dump_db()
    assert result2["s"] == "nao_e_oid"


def test_model_dump_db_none_and_lists_of_models():
    class Sub(MainBaseModel):
        x: int

    class ListModel(MainBaseModel):
        items: list[Sub]
        nulo: None | str

    obj = ListModel(items=[Sub(x=3), Sub(x=7)], nulo=None)
    result = obj.model_dump_db()
    assert result["items"] == [{"x": 3}, {"x": 7}]
    assert "nulo" in result and result["nulo"] is None


def test_model_dump_db_list_of_references():
    class Ref(DbModel):
        field: int
        _collection: ClassVar = "refs"

    class Holder(DbModel):
        items: list[Ref | Id]
        _collection: ClassVar = "holder"

    oid1 = ObjectId()
    oid2 = ObjectId()
    ref1 = Ref(id=oid1, field=10)
    ref2 = Ref(id=oid2, field=20)
    holder = Holder(items=[ref1, oid2])
    result = holder.model_dump_db()
    assert result["items"] == [oid1, oid2]
