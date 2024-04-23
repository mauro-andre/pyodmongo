from ..models.query_operators import LogicalOperator, ComparisonOperator


def and_(*operators: tuple[ComparisonOperator | LogicalOperator]) -> LogicalOperator:
    """
    Creates a logical AND operator to combine multiple comparison or logical operators into a single query condition.

    Args:
        *operators (tuple[ComparisonOperator | LogicalOperator]): A tuple of comparison or logical operators
            that need to be satisfied simultaneously.

    Returns:
        LogicalOperator: A logical operator configured to perform an AND operation on the provided operators.

    Description:
        This function takes multiple query conditions and combines them such that all conditions
        must be true for the query to return results. It is useful for building complex queries
        with multiple conditions that must all be met.
    """
    return LogicalOperator(operator="$and", operators=operators)


def or_(*operators: tuple[ComparisonOperator | LogicalOperator]) -> LogicalOperator:
    """
    Creates a logical OR operator to combine multiple comparison or logical operators into a single query condition.

    Args:
        *operators (tuple[ComparisonOperator | LogicalOperator]): A tuple of comparison or logical operators
            where satisfying any one of them is sufficient.

    Returns:
        LogicalOperator: A logical operator configured to perform an OR operation on the provided operators.

    Description:
        This function is used to build queries where any one of the specified conditions being true will
        make the query return results. It facilitates constructing queries with alternative conditions.
    """
    return LogicalOperator(operator="$or", operators=operators)


def nor(*operators: tuple[ComparisonOperator | LogicalOperator]) -> LogicalOperator:
    """
    Creates a logical NOR operator to combine multiple comparison or logical operators into a single query condition
    that negates all the specified conditions.

    Args:
        *operators (tuple[ComparisonOperator | LogicalOperator]): A tuple of comparison or logical operators
            that should not be satisfied for the query to return results.

    Returns:
        LogicalOperator: A logical operator configured to perform a NOR operation on the provided operators.

    Description:
        The NOR function is useful for constructing queries where the result set should exclude documents that
        meet any of the specified conditions. It effectively negates the conditions put forth by the operators.
    """
    return LogicalOperator(operator="$nor", operators=operators)
