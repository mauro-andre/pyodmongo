from pydantic import BaseModel
from .db_field_info import DbField
from typing import Any


class ComparisonOperator(BaseModel):
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


class _LogicalOperator(BaseModel):
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
    operators: tuple[ComparisonOperator, ...]


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

    operators: tuple[ComparisonOperator | _LogicalOperator, ...]
