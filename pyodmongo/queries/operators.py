from ..models.query_operators import (
    ComparisonOperator,
    LogicalOperator,
    ElemMatchOperator,
)
from ..models.sort_operators import SortOperator
from ..models.db_field_info import DbField
from typing import Any


def eq(field: DbField, value: Any) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the equality ('$eq') operation.

    Args:
        field (DbField): The database field to compare.
        value (Any): The value to compare the field against.

    Returns:
        ComparisonOperator: The comparison operator for the equality operation.
    """
    return field.comparison_operator(operator="$eq", value=value)


def gt(field: DbField, value: Any) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the greater than ('$gt') operation.

    Args:
        field (DbField): The database field to compare.
        value (Any): The value to compare the field against.

    Returns:
        ComparisonOperator: The comparison operator for the greater than operation.
    """
    return field.comparison_operator(operator="$gt", value=value)


def gte(field: DbField, value: Any) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the greater than or equal ('$gte') operation.

    Args:
        field (DbField): The database field to compare.
        value (Any): The value to compare the field against.

    Returns:
        ComparisonOperator: The comparison operator for the greater than or equal operation.
    """
    return field.comparison_operator(operator="$gte", value=value)


def in_(field: DbField, value: list[Any]) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the in ('$in') operation.

    Args:
        field (DbField): The database field to compare.
        value (list[Any]): The list of values to compare the field against.

    Returns:
        ComparisonOperator: The comparison operator for the in operation.
    """
    return field.comparison_operator(operator="$in", value=value)


def lt(field: DbField, value: Any) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the less than ('$lt') operation.

    Args:
        field (DbField): The database field to compare.
        value (Any): The value to compare the field against.

    Returns:
        ComparisonOperator: The comparison operator for the less than operation.
    """
    return field.comparison_operator(operator="$lt", value=value)


def lte(field: DbField, value: Any) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the less than or equal ('$lte') operation.

    Args:
        field (DbField): The database field to compare.
        value (Any): The value to compare the field against.

    Returns:
        ComparisonOperator: The comparison operator for the less than or equal operation.
    """
    return field.comparison_operator(operator="$lte", value=value)


def ne(field: DbField, value: Any) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the not equal ('$ne') operation.

    Args:
        field (DbField): The database field to compare.
        value (Any): The value to compare the field against.

    Returns:
        ComparisonOperator: The comparison operator for the not equal operation.
    """
    return field.comparison_operator(operator="$ne", value=value)


def nin(field: DbField, value: list[Any]) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the not in ('$nin') operation.

    Args:
        field (DbField): The database field to compare.
        value (list[Any]): The list of values to compare the field against.

    Returns:
        ComparisonOperator: The comparison operator for the not in operation.
    """
    return field.comparison_operator(operator="$nin", value=value)


def text(value: Any) -> ComparisonOperator:
    """
    Creates a ComparisonOperator for the text search ('$text' with '$search') operation.

    Args:
        value (Any): The value to search for in the text search.

    Returns:
        ComparisonOperator: The comparison operator for the text search operation.
    """
    return ComparisonOperator(path_str="$text", operator="$search", value=f'"{value}"')


def and_(*operators: ComparisonOperator | LogicalOperator) -> LogicalOperator:
    """
    Creates a LogicalOperator for the logical AND ('$and') operation.

    Args:
        *operators (ComparisonOperator | LogicalOperator): Variable length argument list
            of comparison or logical operators to be combined with logical AND.

    Returns:
        LogicalOperator: The logical operator for the AND operation.
    """
    return LogicalOperator(operator="$and", operators=operators)


def or_(*operators: ComparisonOperator | LogicalOperator) -> LogicalOperator:
    """
    Creates a LogicalOperator for the logical OR ('$or') operation.

    Args:
        *operators (ComparisonOperator | LogicalOperator): Variable length argument list
            of comparison or logical operators to be combined with logical OR.

    Returns:
        LogicalOperator: The logical operator for the OR operation.
    """
    return LogicalOperator(operator="$or", operators=operators)


def nor(*operators: ComparisonOperator | LogicalOperator) -> LogicalOperator:
    """
    Creates a LogicalOperator for the logical NOR ('$nor') operation.

    Args:
        *operators (ComparisonOperator | LogicalOperator): Variable length argument list
            of comparison or logical operators to be combined with logical NOR.

    Returns:
        LogicalOperator: The logical operator for the NOR operation.
    """
    return LogicalOperator(operator="$nor", operators=operators)


def elem_match(
    *operators: ComparisonOperator | LogicalOperator,
    field: DbField,
) -> ElemMatchOperator:
    """
    Creates an ElemMatchOperator for the '$elemMatch' operation, used to match
    documents that contain an array field with at least one element that matches
    the specified criteria.

    Args:
        *operators (ComparisonOperator | LogicalOperator): Variable length argument list
            of comparison or logical operators defining the matching criteria.
        field (DbField): The field to which the elemMatch operation applies.

    Returns:
        ElemMatchOperator: The operator for the elemMatch operation.
    """
    return ElemMatchOperator(field=field, operators=operators)


def sort(*operators: tuple[DbField, int]) -> SortOperator:
    """
    Creates a SortOperator object for MongoDB queries that specifies the sorting order of documents.

    Args:
        *operators (tuple[DbField, int]): Variable length argument list where each tuple contains
            a DbField and an integer. The DbField specifies the field to sort by, and the integer
            specifies the direction (1 for ascending, -1 for descending).

    Returns:
        SortOperator: An object encapsulating the sorting criteria for MongoDB queries.

    Description:
        This function takes one or more sorting criteria represented by tuples of DbField and direction.
        It constructs a SortOperator that is used to define the order in which documents should be returned
        in a query, aligning with MongoDB's sorting syntax. This operator can be used in database operations
        to sort query results according to specified fields and directions.
    """
    return SortOperator(operators=operators)
