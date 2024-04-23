from pydantic import BaseModel
from .id_model import Id


class SaveResponse(BaseModel):
    """
    Represents the response from a save operation (insert or update) in PyODMongo. This
    model provides detailed feedback on the outcome of the operation, including information
    about the number of documents matched, modified, and any document that was upserted.

    Attributes:
        acknowledged (bool): Indicates whether the database operation was acknowledged.
                             If false, the operation may not have been performed.
        matched_count (int): The number of documents that matched the filter in an update
                             operation. This will be zero for insert operations.
        modified_count (int): The number of documents that were actually modified as a
                              result of an update operation.
        upserted_id (Id): The ID of the document that was upserted if an upsert took place;
                          otherwise, None. An upsert is an operation that updates a document
                          if it exists, or inserts a new document if it does not.
    """

    acknowledged: bool
    matched_count: int
    modified_count: int
    upserted_id: Id


class DeleteResponse(BaseModel):
    """
    Represents the response from a delete operation in PyODMongo. This model details the
    outcome of the operation, specifically indicating the count of documents deleted and
    whether the operation was acknowledged by the database.

    Attributes:
        acknowledged (bool): Indicates whether the database operation was acknowledged.
                             If false, the operation may not have been carried out.
        deleted_count (int): The number of documents that were successfully deleted as a
                             result of the operation.
    """

    acknowledged: bool
    deleted_count: int
