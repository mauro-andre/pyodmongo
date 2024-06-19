from pydantic import BaseModel
from typing import Any


class QueryOperator(BaseModel):
    """
    Base model for operators used in PyODMongo queries. Provides the foundational
    structure for combining query conditions using logical operators.

    Methods:
        __and__(self, value): Combines the current operator with another using
                              the logical AND ('$and') operator.
        __or__(self, value): Combines the current operator with another using
                             the logical OR ('$or') operator.
    """

    def __and__(self, value):
        return LogicalOperator(operator="$and", operators=(self, value))

    def __or__(self, value):
        return LogicalOperator(operator="$or", operators=(self, value))

    def to_dict(self): ...


class ComparisonOperator(QueryOperator):
    """
    Represents a single comparison operation in a PyODMongo query, containing a field
    path, an operator, and a value. This model is used to construct query conditions
    that specify how individual fields should be compared to given values.

    Attributes:
        path_str (str): The string representation of the path to the field in the database
                        document, used to identify the field to which the operation applies.
        operator (str): The comparison operator (e.g., '$eq', '$gt', '$lt', etc.) that
                        defines the type of comparison to be performed.
        value (Any): The value to compare against the field specified by path_str. The type
                     of this value can vary depending on the field type and the specific
                     operation being performed.
    """

    path_str: str
    operator: str
    value: Any

    def to_dict(self):
        return {self.path_str: {self.operator: self.value}}


class _LogicalOperator(QueryOperator):
    """
    A base model for logical operators used in PyODMongo queries. This class is not
    intended to be used directly but is extended to support complex logical structures
    combining multiple comparison operations.

    Attributes:
        operator (str): The logical operator (e.g., '$and', '$or') that specifies how
                        the included operators are combined.
        operators (tuple[ComparisonOperator, ...]): A tuple of comparison operators
                        that are to be logically combined according to the `operator`.
    """

    operator: str
    operators: tuple[Any, ...]

    def to_dict(self):
        acu_list = []
        for op in self.operators:
            acu_list.append(op.to_dict())
        return {self.operator: acu_list}


class LogicalOperator(_LogicalOperator):
    """
    Extends _LogicalOperator to allow nested logical operations in PyODMongo queries.
    This class supports including both basic comparison operators and other nested
    logical operators, providing flexibility in defining complex query conditions.

    Attributes:
        operators (tuple[ComparisonOperator | _LogicalOperator, ...]): A tuple containing
                          either comparison operators or other logical operators, allowing
                          for nested logical structures. This enables the construction of
                          intricate query logic necessary for advanced database operations.
    """

    operators: tuple[Any, ...]


class ElemMatchOperator(QueryOperator):
    """
    Represents an $elemMatch operation in a PyODMongo query, used to match documents
    containing an array field with at least one element that matches the specified
    criteria.

    Attributes:
        field (Any): The field on which the $elemMatch operation is applied. This
                     typically represents the path to an array field in the database
                     document.
        operators (tuple[ComparisonOperator | _LogicalOperator, ...]): A tuple of comparison
                     operators and/or logical operators that define the matching criteria
                     for elements within the array.
    """

    field: Any
    operators: tuple[Any, ...]

    def to_dict(self):
        elem_match = {}
        for op in self.operators:
            for key, value in op.to_dict().items():
                elem_match[key] = value
        return {self.field.path_str: {"$elemMatch": elem_match}}
