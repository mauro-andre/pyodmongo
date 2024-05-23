from pydantic import BaseModel
from .db_field_info import DbField


class SortOperator(BaseModel):
    """
    Represents a sort operation in a PyODMongo query, allowing for the specification
    of sorting criteria on database fields. This model is used to construct the sorting
    part of a query, defining how the results should be ordered.

    Attributes:
        operators (tuple[tuple[DbField, int], ...]): A tuple of tuples, where each
                     inner tuple contains a DbField and an integer indicating the
                     sort order. The integer should be 1 for ascending order and -1
                     for descending order.

    Methods:
        to_dict(): Converts the sort operation to a dictionary format suitable for
                   use in a MongoDB query. Validates that the sort order values are
                   either 1 or -1.
    """

    operators: tuple[tuple[DbField, int], ...]

    def to_dict(self):
        dct = {}
        for operator in self.operators:
            if operator[1] not in (1, -1):
                raise ValueError("Only values 1 ascending and -1 descending are valid")
            dct[operator[0].path_str] = operator[1]
        return dct
