from pyodmongo import BaseModel, ConfigDict


class ResponsePaginate(BaseModel):
    current_page: int
    page_quantity: int
    docs_quantity: int
    docs: list
    model_config = ConfigDict(str_strip_whitespace=True)

