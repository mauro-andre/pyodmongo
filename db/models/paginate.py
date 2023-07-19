from .main_model import MainModel


class ResponsePaginate(MainModel):
    current_page: int
    page_quantity: int
    docs_quantity: int
    docs: list
