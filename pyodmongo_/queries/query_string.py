from ..models.db_field_info import DbFieldInfo
from .comparison_operators import comparison_operator
from .logical_operators import and_


def get_field_info(Model, field_name):
    return eval('Model.' + field_name)


def mount_query_filter(items: dict, Model, operators: list):
    for key, value in items.items():
        value = value.strip()
        if value == '':
            continue
        split_result = key.strip().rsplit(sep='_', maxsplit=1)
        operator = f'${split_result[-1]}'
        if operator not in ['$eq', '$gt', '$gte', '$in', '$lt', '$lte', '$ne', '$nin']:
            continue
        try:
            value = eval(value)
        except (SyntaxError, NameError):
            value = value
        field_name = split_result[0]
        try:
            field_info: DbFieldInfo = get_field_info(Model=Model, field_name=field_name)
        except AttributeError:
            raise AttributeError(f"There's no field '{field_name}'")
        operators.append(comparison_operator(field_info=field_info, operator=operator, value=value))
    if len(operators) == 0:
        return {}
    return and_(*operators)
