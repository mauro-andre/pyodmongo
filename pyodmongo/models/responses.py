from pydantic import BaseModel
from .id_model import Id


class DbResponse(BaseModel):
    """
    A class representing the response from database operations.

    Attributes:
        acknowledged (bool): Whether the operation was acknowledged by the server.
        deleted_count (int): The number of documents deleted.
        inserted_count (int): The number of documents inserted.
        matched_count (int): The number of documents matched by the query.
        modified_count (int): The number of documents modified.
        upserted_count (int): The number of documents upserted (inserted or replaced).
        upserted_ids (dict[int, Id]): A dictionary mapping index to the upserted document IDs.
    """

    acknowledged: bool
    deleted_count: int
    inserted_count: int
    matched_count: int
    modified_count: int
    upserted_count: int
    upserted_ids: dict[int, Id]
