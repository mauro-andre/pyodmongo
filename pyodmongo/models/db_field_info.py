from typing import Any
from dataclasses import dataclass


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
