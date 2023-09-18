from ..models.query_operators import ComparisonOperator, LogicalOperator, _LogicalOperator


def comparison_operator_dict(co: ComparisonOperator):
    return {co.path_str: {co.operator: co.value}}


def query_dict(query_operator: ComparisonOperator | LogicalOperator, dct: dict):
    if isinstance(query_operator, ComparisonOperator):
        return comparison_operator_dict(co=query_operator)
    dct[query_operator.operator] = []
    for operator in query_operator.operators:
        if isinstance(operator, ComparisonOperator):
            dct[query_operator.operator].append(comparison_operator_dict(co=operator))
        else:
            dct[query_operator.operator].append(query_dict(query_operator=operator, dct={}))
    return dct
