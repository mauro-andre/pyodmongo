from ..models.db_model import DbModel
from ..models.db_field_info import DbField
from ..models.query_operators import QueryOperator
from .operators import and_, sort
from typing import Type
from datetime import datetime
import re


def is_inheritance_of_db_model(Model):
    """
    Checks if the provided class is a subclass of DbModel or is DbModel itself.

    Args:
        Model (type): The class to check for inheritance.

    Returns:
        bool: True if the class is DbModel or a subclass of DbModel, False otherwise.

    Description:
        This function recursively checks the inheritance chain of the provided class to
        determine if it is derived from DbModel. This is used to ensure that models used
        in database operations inherit from the base DbModel class, enforcing a certain
        structure.
    """
    if Model == DbModel:
        return True
    bases = Model.__bases__
    for base in bases:
        if is_inheritance_of_db_model(Model=base):
            return True
    return False


def js_regex_to_python(js_regex_str):
    """
    Converts a JavaScript-style regex string to a Python regex pattern.

    Args:
        js_regex_str (str): The JavaScript regex string to convert.

    Returns:
        Pattern: A compiled Python regex pattern, or the original string if conversion is not possible.

    Description:
        This function attempts to parse a JavaScript regex string and convert it into a Python
        regex pattern. JavaScript flags are converted to their Python equivalents where applicable.
        If the string cannot be parsed as a JavaScript regex, the original string is returned.
    """
    try:
        match = re.match(r"/([^/]+)/([a-z]*)$", js_regex_str)
    except TypeError:
        return js_regex_str
    try:
        pattern, js_flags = match.groups()
    except AttributeError:
        return js_regex_str
    flags = 0
    if "i" in js_flags:
        flags |= re.IGNORECASE
    if "m" in js_flags:
        flags |= re.MULTILINE
    if "s" in js_flags:
        flags |= re.DOTALL

    return re.compile(pattern, flags)


def mount_query_filter(
    Model: Type[DbModel],
    items: dict,
    initial_comparison_operators: list[QueryOperator],
) -> QueryOperator:
    """
    Constructs a MongoDB query filter from a dictionary of conditions and initializes
    additional comparison operators based on the Model's field definitions.

    Args:
        Model (Type[DbModel]): The model class that fields are checked against.
        items (dict): A dictionary containing field names and their corresponding filter values.
        initial_comparison_operators (list[ComparisonOperator]): A list to which new comparison
            operators are added.

    Returns:
        LogicalOperator, sort_operators: A logical operator combining all comparison operators,
            and sorting operators if '$sort' is found in the keys.

    Raises:
        TypeError: If the Model is not a subclass of DbModel.
        AttributeError: If a field specified does not exist in the Model.

    Description:
        This function interprets and converts query conditions specified in `items` into
        MongoDB query operators. It supports conversion of ISO date strings, evaluation of
        strings into Python expressions, and handling of JavaScript-style regex patterns.
        It also processes sorting instructions if provided.
    """
    is_inheritance = is_inheritance_of_db_model(Model=Model)
    if not is_inheritance:
        raise TypeError("Model must be a DbModel")
    sort_operators = None
    for key, value in items.items():
        value = value.strip()
        if value == "":
            continue
        split_result = key.strip().rsplit(sep="_", maxsplit=1)
        operator = f"${split_result[-1]}"
        if operator not in ["$eq", "$gt", "$gte", "$in", "$lt", "$lte", "$ne", "$nin"]:
            if operator in ["$sort"]:
                value = eval(value)
                for v in value:
                    v[0] = getattr(Model, v[0])
                sort_operators = sort(*value)
            continue
        try:
            value = datetime.fromisoformat(value)
        except (TypeError, ValueError):
            try:
                value = eval(value)
            except (NameError, SyntaxError):
                value = value
        field_name = split_result[0]
        if type(value) is list:
            for index, item in enumerate(value):
                value[index] = js_regex_to_python(item)
        try:
            db_field_info: DbField = eval("Model." + field_name)
        except AttributeError:
            raise AttributeError(f"There's no field '{field_name}' in {Model.__name__}")
        initial_comparison_operators.append(
            db_field_info.comparison_operator(operator=operator, value=value)
        )
    if len(initial_comparison_operators) == 0:
        return None, sort_operators
    return and_(*initial_comparison_operators), sort_operators
