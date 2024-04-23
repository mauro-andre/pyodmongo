from ..models.query_operators import ComparisonOperator, LogicalOperator
from ..models.sort_operators import SortOperator


def comparison_operator_dict(co: ComparisonOperator):
    """
    Converts a ComparisonOperator instance into a dictionary format suitable for MongoDB queries.

    Args:
        co (ComparisonOperator): An instance of ComparisonOperator specifying the field, operator,
                                 and value for a query condition.

    Returns:
        dict: A dictionary representing the MongoDB query condition, formatted as {field_path: {operator: value}}.

    Description:
        This function takes a ComparisonOperator which includes details like the path to the field,
        the MongoDB comparison operator (e.g., "$eq", "$gt"), and the value for the operation, and converts
        it into the dictionary format that MongoDB expects for query operations.
    """
    return {co.path_str: {co.operator: co.value}}


def query_dict(query_operator: ComparisonOperator | LogicalOperator, dct: dict) -> dict:
    """
    Recursively builds a dictionary representation of query conditions from nested ComparisonOperator
    and LogicalOperator instances.

    Args:
        query_operator (ComparisonOperator | LogicalOperator): The operator that defines part of a MongoDB query.
        dct (dict): The dictionary to which the query condition is added. This is mainly used internally
                    for recursive calls.

    Returns:
        dict: A dictionary representing a complex MongoDB query with possible nested conditions.

    Description:
        This function handles both simple comparison conditions and complex logical groupings (e.g., "$and", "$or").
        It recursively constructs a nested dictionary structure that MongoDB uses to execute complex queries involving
        multiple conditions and logical operators.
    """
    if isinstance(query_operator, ComparisonOperator):
        return comparison_operator_dict(co=query_operator)
    dct[query_operator.operator] = []
    for operator in query_operator.operators:
        if isinstance(operator, ComparisonOperator):
            dct[query_operator.operator].append(comparison_operator_dict(co=operator))
        else:
            dct[query_operator.operator].append(
                query_dict(query_operator=operator, dct={})
            )
    return dct


def sort_dict(sort_operators: SortOperator) -> dict:
    """
    Converts a SortOperator into a dictionary format suitable for MongoDB sort operations.

    Args:
        sort_operators (SortOperator): An instance of SortOperator containing one or more sorting criteria.

    Returns:
        dict: A dictionary representing the sorting criteria for a MongoDB operation.

    Description:
        This function translates sorting instructions encapsulated by SortOperator instances into a dictionary
        where keys are field paths and values are the sort directions (1 for ascending, -1 for descending).
        This format is used by MongoDB to determine the order of documents returned by a query.
    """
    dct = {}
    for operator in sort_operators.operators:
        if operator[1] not in (1, -1):
            raise ValueError("Only values 1 ascending and -1 descending are valid")
        dct[operator[0].path_str] = operator[1]
    return dct
