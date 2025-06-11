from pyodmongo.v2.aggregation import operators
from pyodmongo.v2 import DbModel


def test_aggregation_operators():
    class MyModel(DbModel):
        attr_str: str
        attr_int: int

    # == operator
    assert operators.eq(MyModel.attr_str, "abc") == {"$eq": ["attr_str", "abc"]}
    assert operators.eq(MyModel.attr_int, 42) == {"$eq": ["attr_int", 42]}

    # != operator
    assert operators.ne(MyModel.attr_str, "def") == {"$ne": ["attr_str", "def"]}
    assert operators.ne(MyModel.attr_int, 7) == {"$ne": ["attr_int", 7]}

    # < operator
    assert operators.lt(MyModel.attr_str, "zzz") == {"$lt": ["attr_str", "zzz"]}
    assert operators.lt(MyModel.attr_int, 100) == {"$lt": ["attr_int", 100]}

    # <= operator
    assert operators.lte(MyModel.attr_str, "zzz") == {"$lte": ["attr_str", "zzz"]}
    assert operators.lte(MyModel.attr_int, 101) == {"$lte": ["attr_int", 101]}

    # > operator
    assert operators.gt(MyModel.attr_str, "aaa") == {"$gt": ["attr_str", "aaa"]}
    assert operators.gt(MyModel.attr_int, 0) == {"$gt": ["attr_int", 0]}

    # >= operator
    assert operators.gte(MyModel.attr_str, "abc") == {"$gte": ["attr_str", "abc"]}
    assert operators.gte(MyModel.attr_int, 42) == {"$gte": ["attr_int", 42]}

    # Logical operators
    eq1 = operators.eq(MyModel.attr_str, "abc")
    gt1 = operators.gt(MyModel.attr_int, 5)
    lt1 = operators.lt(MyModel.attr_int, 100)

    # and_
    assert operators.and_(eq1, gt1, lt1) == {"$and": [eq1, gt1, lt1]}
    assert operators.and_() == {"$and": []}

    # or_
    assert operators.or_(eq1, gt1) == {"$or": [eq1, gt1]}
    assert operators.or_() == {"$or": []}

    # nor
    assert operators.nor(eq1, gt1) == {"$nor": [eq1, gt1]}
    assert operators.nor() == {"$nor": []}

    # not_
    assert operators.not_(eq1) == {"$not": [eq1]}

    # in_ operator
    assert operators.in_(MyModel.attr_str, ["a", "b", "c"]) == {
        "$in": ["attr_str", ["a", "b", "c"]]
    }
    assert operators.in_(MyModel.attr_int, [1, 2, 3]) == {
        "$in": ["attr_int", [1, 2, 3]]
    }

    # nin operator
    assert operators.nin(MyModel.attr_str, ["x", "y"]) == {
        "$nin": ["attr_str", ["x", "y"]]
    }
    assert operators.nin(MyModel.attr_int, []) == {"$nin": ["attr_int", []]}
