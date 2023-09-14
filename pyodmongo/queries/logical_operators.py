from ..models.query_operators import LogicalOperator, ComparisonOperator


def and_(*operators: tuple[ComparisonOperator]) -> LogicalOperator:
    return LogicalOperator(operator='$and', comparison_operators=operators)


def or_(*operators: tuple[ComparisonOperator]) -> LogicalOperator:
    return LogicalOperator(operator='$or', comparison_operators=operators)


def nor(*operators: tuple[ComparisonOperator]) -> LogicalOperator:
    return LogicalOperator(operator='$nor', comparison_operators=operators)
