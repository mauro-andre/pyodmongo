from ..models.query_operators import LogicalOperator, ComparisonOperator


def and_(*operators: tuple[ComparisonOperator | LogicalOperator]) -> LogicalOperator:
    return LogicalOperator(operator='$and', operators=operators)


def or_(*operators: tuple[ComparisonOperator | LogicalOperator]) -> LogicalOperator:
    return LogicalOperator(operator='$or', operators=operators)


def nor(*operators: tuple[ComparisonOperator | LogicalOperator]) -> LogicalOperator:
    return LogicalOperator(operator='$nor', operators=operators)
