from ..models.db_field_info import DbField
from ..models.sort_operators import SortOperator


def sort(*operators: tuple[DbField, int]) -> SortOperator:
    """
    Creates a SortOperator object for MongoDB queries that specifies the sorting order of documents.

    Args:
        *operators (tuple[DbField, int]): Variable length argument list where each tuple contains
            a DbField and an integer. The DbField specifies the field to sort by, and the integer
            specifies the direction (1 for ascending, -1 for descending).

    Returns:
        SortOperator: An object encapsulating the sorting criteria for MongoDB queries.

    Description:
        This function takes one or more sorting criteria represented by tuples of DbField and direction.
        It constructs a SortOperator that is used to define the order in which documents should be returned
        in a query, aligning with MongoDB's sorting syntax. This operator can be used in database operations
        to sort query results according to specified fields and directions.
    """
    return SortOperator(operators=operators)
