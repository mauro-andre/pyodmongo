from pyodmongo.services.verify_subclasses import is_subclass
from pyodmongo import DbModel, MainBaseModel
from pyodmongo.models.query_operators import (
    QueryOperator,
    LogicalOperator,
    _LogicalOperator,
    ComparisonOperator,
    ElemMatchOperator,
)


def test_is_subclass():
    assert is_subclass(class_to_verify=QueryOperator, subclass=QueryOperator) is True
    assert is_subclass(class_to_verify=LogicalOperator, subclass=QueryOperator) is True
    assert is_subclass(class_to_verify=_LogicalOperator, subclass=QueryOperator) is True
    assert (
        is_subclass(class_to_verify=ComparisonOperator, subclass=QueryOperator) is True
    )
    assert (
        is_subclass(class_to_verify=ElemMatchOperator, subclass=QueryOperator) is True
    )
    assert is_subclass(class_to_verify=DbModel, subclass=QueryOperator) is False
    assert is_subclass(class_to_verify=MainBaseModel, subclass=QueryOperator) is False
