from typing import Any
from dataclasses import dataclass
from .query_operators import ComparisonOperator
from .id_model import Id
from bson import ObjectId


@dataclass
class DbField:
    """
    Represents a field within a database model, containing metadata necessary for
    managing the serialization and deserialization of model fields, especially in
    contexts involving references to other documents or complex nested structures.

    Attributes:
        field_name (str | None): The name of the field as defined in the database model.
        field_alias (str | None): The alias used for the field in database operations,
                                  which might differ from the field name.
        path_str (str | None): The string representation of the path to the field within
                               nested structures or related models.
        field_type (Any | None): The data type of the field, which can be any valid Python
                                 type or a more complex custom type.
        by_reference (bool | None): Indicates whether the field is linked by reference
                                    to another document or model, rather than embedded.
        is_list (bool | None): Specifies if the field is expected to be a list of items,
                               typically used for handling multiple relationships or
                               collections of values.
        has_model_fields (bool | None): Indicates if the field itself contains sub-fields
                                        that are also modeled, suggesting a nested data
                                        structure that requires special handling.
    """

    field_name: str = None
    field_alias: str = None
    path_str: str = None
    field_type: Any = None
    by_reference: bool = None
    is_list: bool = None
    has_model_fields: bool = None

    def comparison_operator(self, operator: str, value: Any) -> ComparisonOperator:
        if self.by_reference or self.field_type == Id:
            if type(value) != list and value is not None:
                value = ObjectId(value)
            if type(value) == list:
                value = [ObjectId(v) for v in value]
        return ComparisonOperator(
            path_str=self.path_str, operator=operator, value=value
        )

    def __lt__(self, value: Any) -> ComparisonOperator:
        return self.comparison_operator(operator="$lt", value=value)

    def __le__(self, value: Any) -> ComparisonOperator:
        return self.comparison_operator(operator="$lte", value=value)

    def __eq__(self, value: Any) -> ComparisonOperator:
        if isinstance(value, DbField):
            return super().__eq__(value)
        return self.comparison_operator(operator="$eq", value=value)

    def __ne__(self, value: Any) -> ComparisonOperator:
        if isinstance(value, DbField):
            return super().__ne__(value)
        return self.comparison_operator(operator="$ne", value=value)

    def __gt__(self, value: Any) -> ComparisonOperator:
        return self.comparison_operator(operator="$gt", value=value)

    def __ge__(self, value: Any) -> ComparisonOperator:
        return self.comparison_operator(operator="$gte", value=value)
