from pydantic import BaseModel
from .id_model import Id


class SaveResponse(BaseModel):
    acknowledged: bool
    matched_count: int
    modified_count: int
    upserted_id: Id


class DeleteResponse(BaseModel):
    acknowledged: bool
    deleted_count: int
