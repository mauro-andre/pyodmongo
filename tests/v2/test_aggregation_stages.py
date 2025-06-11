from pyodmongo.v2.aggregation import stages, operators
from pyodmongo.v2 import DbModel


class MyModel(DbModel):
    attr: int
    status: str
    group: str


def test_match():

    # Using a raw dict
    assert stages.match({"field": "value"}) == {"$match": {"field": "value"}}
    # Using operators.eq
    assert stages.match(operators.eq(MyModel.status, "A")) == {
        "$match": {"$eq": ["status", "A"]}
    }
    # Using operators.gt
    assert stages.match(operators.gt(MyModel.attr, 5)) == {
        "$match": {"$gt": ["attr", 5]}
    }


def test_project():
    assert stages.project({"field1": 1, "field2": 0}) == {
        "$project": {"field1": 1, "field2": 0}
    }
    # Using more complex projection with operators
    assert stages.project({"my_field": operators.gt(MyModel.attr, 10)}) == {
        "$project": {"my_field": {"$gt": ["attr", 10]}}
    }


def test_group():
    assert stages.group({"_id": "$cat", "count": {"$sum": 1}}) == {
        "$group": {"_id": "$cat", "count": {"$sum": 1}}
    }
    # Using an expression as _id with an operator
    assert stages.group(
        {"_id": operators.eq(MyModel.group, "X"), "amount": {"$sum": "$attr"}}
    ) == {"$group": {"_id": {"$eq": ["group", "X"]}, "amount": {"$sum": "$attr"}}}


def test_sort():
    assert stages.sort({"field": 1, "another": -1}) == {
        "$sort": {"field": 1, "another": -1}
    }
    # Sorting is static with respect to operators, so no direct usage shown here


def test_limit():
    assert stages.limit(5) == {"$limit": 5}


def test_skip():
    assert stages.skip(3) == {"$skip": 3}


def test_unwind():
    assert stages.unwind("$list_field") == {"$unwind": "$list_field"}


def test_add_fields():
    assert stages.add_fields({"result": {"$add": ["$a", "$b"]}}) == {
        "$addFields": {"result": {"$add": ["$a", "$b"]}}
    }
    # Using operators.in_ as field value
    assert stages.add_fields({"is_valid": operators.in_(MyModel.attr, [1, 2, 3])}) == {
        "$addFields": {"is_valid": {"$in": ["attr", [1, 2, 3]]}}
    }


def test_lookup_simple():
    # Dict classic form
    assert stages.lookup(
        from_collection="inventory",
        local_field="item",
        foreign_field="sku",
        as_field="inventory_docs",
    ) == {
        "$lookup": {
            "from": "inventory",
            "localField": "item",
            "foreignField": "sku",
            "as": "inventory_docs",
        }
    }


def test_lookup_pipeline_with_dict():
    # Pipeline form with just a dict
    assert stages.lookup(
        from_collection="orders",
        pipeline=[{"$match": {"status": "A"}}],
        as_field="orders_docs",
    ) == {
        "$lookup": {
            "from": "orders",
            "pipeline": [{"$match": {"status": "A"}}],
            "as": "orders_docs",
        }
    }


def test_lookup_pipeline_with_operators():
    # Pipeline form, using operators in pipeline
    assert stages.lookup(
        from_collection="orders",
        pipeline=[
            stages.match(operators.eq(MyModel.status, "A")),
            stages.match(operators.gte(MyModel.attr, 100)),
        ],
        as_field="docs",
    ) == {
        "$lookup": {
            "from": "orders",
            "pipeline": [
                {"$match": {"$eq": ["status", "A"]}},
                {"$match": {"$gte": ["attr", 100]}},
            ],
            "as": "docs",
        }
    }
