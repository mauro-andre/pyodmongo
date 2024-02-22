from pyodmongo import DbModel, Id, Field
from pydantic import BaseModel
from typing import ClassVar
from pprint import pprint


def test_single_class_project_pipeline():
    class A(DbModel):
        a1: str
        a2: str
        _collection: ClassVar = "a"

    expected = [
        {
            "$project": {
                "_id": True,
                "a1": True,
                "a2": True,
                "created_at": True,
                "updated_at": True,
            }
        },
    ]

    assert A._reference_pipeline == expected


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
                                {
                                    "$project": {
                                        "_id": True,
                                        "a1": True,
                                        "created_at": True,
                                        "updated_at": True,
                                    }
                                }
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
                                {
                                    "$project": {
                                        "_id": True,
                                        "a01": True,
                                        "created_at": True,
                                        "updated_at": True,
                                    }
                                }
                            ],
                        }
                    },
                    {"$set": {"b2": {"$arrayElemAt": ["$b2", 0]}}},
                    {
                        "$project": {
                            "_id": True,
                            "b1": True,
                            "b2": True,
                            "created_at": True,
                            "updated_at": True,
                        }
                    },
                ],
            },
        },
        {
            "$project": {
                "_id": True,
                "c1": True,
                "created_at": True,
                "updated_at": True,
            }
        },
    ]
    assert C._reference_pipeline == expected


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
