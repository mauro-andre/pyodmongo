from pyodmongo import DbModel, MainBaseModel, Id
from pydantic import BaseModel
from typing import ClassVar
from pyodmongo.services.reference_pipeline import resolve_reference_pipeline
import pytest


def test_single_class_project_pipeline():
    class A(DbModel):
        a1: str
        a2: str
        _collection: ClassVar = "a"

    expected = [
        # {
        #     "$project": {
        #         "_id": True,
        #         "a1": True,
        #         "a2": True,
        #         "created_at": True,
        #         "updated_at": True,
        #     }
        # },
    ]

    assert (
        resolve_reference_pipeline(cls=A, pipeline=[], populate_db_fields=None)
        == expected
    )


def test_simple_if_reference_pipeline_is_correct():
    class A0(DbModel):
        a01: str
        _collection: ClassVar = "a0"

    class A(DbModel):
        a1: str
        _collection: ClassVar = "a"

    class B(DbModel):
        b1: A | Id
        b2: A0 | Id
        _collection: ClassVar = "b"

    class C(DbModel):
        c1: list[B | Id]
        _collection: ClassVar = "c"

    expected = [
        {
            "$lookup": {
                "as": "c1",
                "foreignField": "_id",
                "from": "b",
                "localField": "c1",
                "pipeline": [
                    {
                        "$lookup": {
                            "as": "b1",
                            "foreignField": "_id",
                            "from": "a",
                            "localField": "b1",
                            "pipeline": [
                                # {
                                #     "$project": {
                                #         "_id": True,
                                #         "a1": True,
                                #         "created_at": True,
                                #         "updated_at": True,
                                #     }
                                # }
                            ],
                        }
                    },
                    {"$set": {"b1": {"$arrayElemAt": ["$b1", 0]}}},
                    {
                        "$lookup": {
                            "as": "b2",
                            "foreignField": "_id",
                            "from": "a0",
                            "localField": "b2",
                            "pipeline": [
                                # {
                                #     "$project": {
                                #         "_id": True,
                                #         "a01": True,
                                #         "created_at": True,
                                #         "updated_at": True,
                                #     }
                                # }
                            ],
                        }
                    },
                    {"$set": {"b2": {"$arrayElemAt": ["$b2", 0]}}},
                    # {
                    #     "$project": {
                    #         "_id": True,
                    #         "b1": True,
                    #         "b2": True,
                    #         "created_at": True,
                    #         "updated_at": True,
                    #     }
                    # },
                ],
            },
        },
        # {
        #     "$project": {
        #         "_id": True,
        #         "c1": True,
        #         "created_at": True,
        #         "updated_at": True,
        #     }
        # },
    ]
    assert (
        resolve_reference_pipeline(cls=C, pipeline=[], populate_db_fields=None)
        == expected
    )


def test_manual_pipeline():
    class MyModel1(DbModel):
        attr1: str
        _collection: ClassVar = "my_model_1"

    class MyModel2(DbModel):
        attr2: str
        my_model_1: MyModel1
        _collection: ClassVar = "my_model_2"
        _pipeline: ClassVar = ["manual pipeline here"]

    assert MyModel1._pipeline == []
    assert MyModel2._pipeline == ["manual pipeline here"]


def test_recursive_reference_pipeline():
    class Zero(DbModel):
        attr_0: str = "Zero"
        _collection: ClassVar = "col_0"

    class A(DbModel):
        attr_1: str = "One"
        zero_1: Zero | Id = Zero()
        zero_2: Zero = Zero()
        _collection: ClassVar = "col_a"

    class B(MainBaseModel):
        attr_2: str = "Two"
        a1: A | Id = A()
        a2: A = A()

    class C(DbModel):
        attr_3: str = "Three"
        a: A | Id = A()
        b: B = B()
        _collection: ClassVar = "col_c"

    assert resolve_reference_pipeline(cls=C, pipeline=[], populate_db_fields=None) == [
        {
            "$lookup": {
                "as": "a",
                "foreignField": "_id",
                "from": "col_a",
                "localField": "a",
                "pipeline": [
                    {
                        "$lookup": {
                            "as": "zero_1",
                            "foreignField": "_id",
                            "from": "col_0",
                            "localField": "zero_1",
                            "pipeline": [
                                # {
                                #     "$project": {
                                #         "_id": True,
                                #         "attr_0": True,
                                #         "created_at": True,
                                #         "updated_at": True,
                                #     }
                                # }
                            ],
                        }
                    },
                    {"$set": {"zero_1": {"$arrayElemAt": ["$zero_1", 0]}}},
                    # {
                    #     "$project": {
                    #         "_id": True,
                    #         "attr_1": True,
                    #         "created_at": True,
                    #         "updated_at": True,
                    #         "zero_1": True,
                    #         "zero_2._id": True,
                    #         "zero_2.attr_0": True,
                    #         "zero_2.created_at": True,
                    #         "zero_2.updated_at": True,
                    #     }
                    # },
                ],
            }
        },
        {"$set": {"a": {"$arrayElemAt": ["$a", 0]}}},
        {
            "$lookup": {
                "as": "b.a1",
                "foreignField": "_id",
                "from": "col_a",
                "localField": "b.a1",
                "pipeline": [
                    {
                        "$lookup": {
                            "as": "zero_1",
                            "foreignField": "_id",
                            "from": "col_0",
                            "localField": "zero_1",
                            "pipeline": [
                                # {
                                #     "$project": {
                                #         "_id": True,
                                #         "attr_0": True,
                                #         "created_at": True,
                                #         "updated_at": True,
                                #     }
                                # }
                            ],
                        }
                    },
                    {"$set": {"zero_1": {"$arrayElemAt": ["$zero_1", 0]}}},
                    # {
                    #     "$project": {
                    #         "_id": True,
                    #         "attr_1": True,
                    #         "created_at": True,
                    #         "updated_at": True,
                    #         "zero_1": True,
                    #         "zero_2._id": True,
                    #         "zero_2.attr_0": True,
                    #         "zero_2.created_at": True,
                    #         "zero_2.updated_at": True,
                    #     }
                    # },
                ],
            }
        },
        {"$set": {"b.a1": {"$arrayElemAt": ["$b.a1", 0]}}},
        {
            "$lookup": {
                "as": "b.a2.zero_1",
                "foreignField": "_id",
                "from": "col_0",
                "localField": "b.a2.zero_1",
                "pipeline": [
                    # {
                    #     "$project": {
                    #         "_id": True,
                    #         "attr_0": True,
                    #         "created_at": True,
                    #         "updated_at": True,
                    #     }
                    # }
                ],
            }
        },
        {"$set": {"b.a2.zero_1": {"$arrayElemAt": ["$b.a2.zero_1", 0]}}},
        # {
        #     "$project": {
        #         "_id": True,
        #         "a": True,
        #         "attr_3": True,
        #         "b.a1": True,
        #         "b.a2._id": True,
        #         "b.a2.attr_1": True,
        #         "b.a2.created_at": True,
        #         "b.a2.updated_at": True,
        #         "b.a2.zero_1": True,
        #         "b.a2.zero_2._id": True,
        #         "b.a2.zero_2.attr_0": True,
        #         "b.a2.zero_2.created_at": True,
        #         "b.a2.zero_2.updated_at": True,
        #         "b.attr_2": True,
        #         "created_at": True,
        #         "updated_at": True,
        #     }
        # },
    ]


def test_main_base_model_usage_recommendation():
    class Z(DbModel):
        z1: str = "z1"
        _collection: TypeError = "z"

    class X(BaseModel):
        x1: str = "x1"
        x2: str = "x2"
        z: Z | Id

    class Y(DbModel):
        y1: str = "y1"
        x: X
        _collection: TypeError = "y"

    with pytest.raises(
        TypeError,
        match="The X class inherits from Pydantic's BaseModel class. Try switching to PyODMongo's MainBaseModel class",
    ):
        resolve_reference_pipeline(cls=Y, pipeline=[], populate_db_fields=None)
