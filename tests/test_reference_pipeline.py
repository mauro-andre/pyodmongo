from pyodmongo import DbModel, MainBaseModel, Id
from pydantic import BaseModel, Field
from typing import ClassVar
from pyodmongo.services.reference_pipeline import (
    resolve_reference_pipeline,
    _paths_to_ref_ids,
)
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
                "from": "b",
                "localField": "c1",
                "foreignField": "_id",
                "as": "c1",
                "pipeline": [
                    {
                        "$lookup": {
                            "from": "a",
                            "localField": "b1",
                            "foreignField": "_id",
                            "as": "b1",
                            "pipeline": [],
                        }
                    },
                    {"$set": {"b1": {"$arrayElemAt": ["$b1", 0]}}},
                    {
                        "$set": {
                            "b1": {
                                "$cond": {
                                    "if": {
                                        "$or": [
                                            {"$eq": ["$b1", None]},
                                            {"$eq": ["$b1", {}]},
                                        ]
                                    },
                                    "then": None,
                                    "else": "$b1",
                                }
                            }
                        }
                    },
                    {
                        "$lookup": {
                            "from": "a0",
                            "localField": "b2",
                            "foreignField": "_id",
                            "as": "b2",
                            "pipeline": [],
                        }
                    },
                    {"$set": {"b2": {"$arrayElemAt": ["$b2", 0]}}},
                    {
                        "$set": {
                            "b2": {
                                "$cond": {
                                    "if": {
                                        "$or": [
                                            {"$eq": ["$b2", None]},
                                            {"$eq": ["$b2", {}]},
                                        ]
                                    },
                                    "then": None,
                                    "else": "$b2",
                                }
                            }
                        }
                    },
                ],
            }
        }
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
                "from": "col_a",
                "localField": "a",
                "foreignField": "_id",
                "as": "a",
                "pipeline": [
                    {
                        "$lookup": {
                            "from": "col_0",
                            "localField": "zero_1",
                            "foreignField": "_id",
                            "as": "zero_1",
                            "pipeline": [],
                        }
                    },
                    {"$set": {"zero_1": {"$arrayElemAt": ["$zero_1", 0]}}},
                    {
                        "$set": {
                            "zero_1": {
                                "$cond": {
                                    "if": {
                                        "$or": [
                                            {"$eq": ["$zero_1", None]},
                                            {"$eq": ["$zero_1", {}]},
                                        ]
                                    },
                                    "then": None,
                                    "else": "$zero_1",
                                }
                            }
                        }
                    },
                ],
            }
        },
        {"$set": {"a": {"$arrayElemAt": ["$a", 0]}}},
        {
            "$set": {
                "a": {
                    "$cond": {
                        "if": {"$or": [{"$eq": ["$a", None]}, {"$eq": ["$a", {}]}]},
                        "then": None,
                        "else": "$a",
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "col_a",
                "localField": "b.a1",
                "foreignField": "_id",
                "as": "b.a1",
                "pipeline": [
                    {
                        "$lookup": {
                            "from": "col_0",
                            "localField": "zero_1",
                            "foreignField": "_id",
                            "as": "zero_1",
                            "pipeline": [],
                        }
                    },
                    {"$set": {"zero_1": {"$arrayElemAt": ["$zero_1", 0]}}},
                    {
                        "$set": {
                            "zero_1": {
                                "$cond": {
                                    "if": {
                                        "$or": [
                                            {"$eq": ["$zero_1", None]},
                                            {"$eq": ["$zero_1", {}]},
                                        ]
                                    },
                                    "then": None,
                                    "else": "$zero_1",
                                }
                            }
                        }
                    },
                ],
            }
        },
        {"$set": {"b.a1": {"$arrayElemAt": ["$b.a1", 0]}}},
        {
            "$set": {
                "b.a1": {
                    "$cond": {
                        "if": {
                            "$or": [{"$eq": ["$b.a1", None]}, {"$eq": ["$b.a1", {}]}]
                        },
                        "then": "$$REMOVE",
                        "else": "$b.a1",
                    }
                }
            }
        },
        {
            "$set": {
                "b": {
                    "$cond": {
                        "if": {"$or": [{"$eq": ["$b", None]}, {"$eq": ["$b", {}]}]},
                        "then": None,
                        "else": "$b",
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "col_0",
                "localField": "b.a2.zero_1",
                "foreignField": "_id",
                "as": "b.a2.zero_1",
                "pipeline": [],
            }
        },
        {"$set": {"b.a2.zero_1": {"$arrayElemAt": ["$b.a2.zero_1", 0]}}},
        {
            "$set": {
                "b.a2.zero_1": {
                    "$cond": {
                        "if": {
                            "$or": [
                                {"$eq": ["$b.a2.zero_1", None]},
                                {"$eq": ["$b.a2.zero_1", {}]},
                            ]
                        },
                        "then": "$$REMOVE",
                        "else": "$b.a2.zero_1",
                    }
                }
            }
        },
        {
            "$set": {
                "b.a2": {
                    "$cond": {
                        "if": {
                            "$or": [{"$eq": ["$b.a2", None]}, {"$eq": ["$b.a2", {}]}]
                        },
                        "then": "$$REMOVE",
                        "else": "$b.a2",
                    }
                }
            }
        },
        {
            "$set": {
                "b": {
                    "$cond": {
                        "if": {"$or": [{"$eq": ["$b", None]}, {"$eq": ["$b", {}]}]},
                        "then": None,
                        "else": "$b",
                    }
                }
            }
        },
    ]


def test_main_base_model_usage_recommendation():
    class Z(DbModel):
        z1: str = "z1"
        _collection: TypeError = "z"

    class X(BaseModel):
        x1: str = "x1"
        x2: str = "x2"
        z: Z | Id

    with pytest.raises(
        TypeError,
        match="The X class inherits from Pydantic's BaseModel class. Try switching to PyODMongo's MainBaseModel class",
    ):
        _paths_to_ref_ids(cls=X, paths=[], db_field_path=[], populate_db_fields=None)
