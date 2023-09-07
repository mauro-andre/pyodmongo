from pydantic import BaseModel


class ResponsePaginate(BaseModel):
    current_page: int
    page_quantity: int
    docs_quantity: int
    docs: list
