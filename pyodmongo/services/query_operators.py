from ..models.query_operators import ComparisonOperator, LogicalOperator, SortOperator


def comparison_operator_dict(co: ComparisonOperator):
    return {co.path_str: {co.operator: co.value}}


def query_dict(query_operator: ComparisonOperator | LogicalOperator, dct: dict) -> dict:
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
    dct = {}
    for operator in sort_operators.operators:
        if operator[1] not in (1, -1):
            raise ValueError("Only values 1 ascending and -1 descending are valid")
        dct[operator[0].path_str] = operator[1]
    return dct
