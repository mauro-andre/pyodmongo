from pydantic import BaseModel
from .id_model import Id


class DbResponse(BaseModel):
    acknowledged: bool
    deleted_count: int
    inserted_count: int
    matched_count: int
    modified_count: int
    upserted_count: int
    upserted_ids: dict[int, Id]
