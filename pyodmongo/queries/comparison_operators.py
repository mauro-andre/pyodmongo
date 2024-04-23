from bson import ObjectId
from ..models.id_model import Id
from ..models.db_field_info import DbField
from ..models.query_operators import ComparisonOperator
from typing import Any


def comparison_operator(
    field: DbField, operator: str, value: Any
) -> ComparisonOperator:
    """
    Creates a ComparisonOperator object for MongoDB queries that involves transforming
    values into ObjectId where necessary, based on the field's configuration.

    Args:
        field (DbField): The field against which the operator is applied.
        operator (str): The MongoDB query operator as a string (e.g., "$eq", "$gt").
        value (Any): The value to compare against the field. This may be converted to ObjectId
                     if the field is a reference or designed to store ObjectIds.

    Returns:
        ComparisonOperator: An object encapsulating the field path, operator, and possibly transformed value.

    Description:
        This function adjusts the comparison value to an ObjectId if the field is a reference or
        explicitly manages ObjectIds, accommodating MongoDB's requirements for certain operations.
        Lists of values are also processed to convert each element to ObjectId where appropriate.
    """
    if field.by_reference or field.field_type == Id:
        if type(value) != list and value is not None:
            value = ObjectId(value)
        if type(value) == list:
            value = [ObjectId(v) for v in value]
    return ComparisonOperator(path_str=field.path_str, operator=operator, value=value)


def eq(field: DbField, value: Any) -> ComparisonOperator:
    """
    Creates an equality comparison operator for the specified field and value.

    Args:
        field (DbField): The field to apply the equality check.
        value (Any): The value to compare for equality.

    Returns:
        ComparisonOperator: A comparison operator configured for an equality check.
    """
    return comparison_operator(field=field, operator="$eq", value=value)


def gt(field: DbField, value) -> ComparisonOperator:
    """Creates a 'greater than' comparison operator."""
    return comparison_operator(field=field, operator="$gt", value=value)


def gte(field: DbField, value) -> ComparisonOperator:
    """Creates a 'greater than or equal to' comparison operator."""
    return comparison_operator(field=field, operator="$gte", value=value)


def in_(field: DbField, value: list) -> ComparisonOperator:
    """
    Creates an 'in' comparison operator to check if the field's value is within the specified list.

    Args:
        field (DbField): The field for the operation.
        value (list): The list of values to check against the field's value.

    Returns:
        ComparisonOperator: Configured for the 'in' operation.
    """
    return comparison_operator(field=field, operator="$in", value=value)


def lt(field: DbField, value) -> ComparisonOperator:
    """Creates a 'less than' comparison operator."""
    return comparison_operator(field=field, operator="$lt", value=value)


def lte(field: DbField, value) -> ComparisonOperator:
    """Creates a 'less than or equal to' comparison operator."""
    return comparison_operator(field=field, operator="$lte", value=value)


def ne(field: DbField, value) -> ComparisonOperator:
    """Creates a 'not equal' comparison operator."""
    return comparison_operator(field=field, operator="$ne", value=value)


def nin(field: DbField, value: list) -> ComparisonOperator:
    """
    Creates a 'not in' comparison operator to check if the field's value is not within the specified list.

    Args:
        field (DbField): The field for the operation.
        value (list): The list of values to check against the field's value.

    Returns:
        ComparisonOperator: Configured for the 'not in' operation.
    """
    return comparison_operator(field=field, operator="$nin", value=value)


def text(value) -> ComparisonOperator:
    """
    Creates a text search comparison operator using MongoDB's `$text` and `$search` to match text within a string field.

    Args:
        value (str): The text string to search for within documents.

    Returns:
        ComparisonOperator: Configured for a text search.
    """
    return ComparisonOperator(path_str="$text", operator="$search", value=f'"{value}"')
