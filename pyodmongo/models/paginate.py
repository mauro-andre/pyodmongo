from pydantic import BaseModel


class ResponsePaginate(BaseModel):
    """
    A model for representing paginated responses specifically tailored for use with
    PyODMongo in applications dealing with large datasets that require efficient data
    retrieval. This class encapsulates essential pagination details along with the
    actual documents (docs) that are being paginated, as retrieved from a MongoDB
    database via PyODMongo queries.

    Attributes:
        current_page (int): The index of the current page being viewed.
        page_quantity (int): The total number of pages available based on the current
                             pagination settings and the total dataset size.
        docs_quantity (int): The number of documents present in the current page.
        docs (list): A list containing the documents of the current page. The specific
                     type and structure of these documents will depend on the application's
                     data model.

    This model can be used to standardize the response format for paginated data across
    different parts of an application, ensuring consistency and ease of integration
    with frontend paging mechanisms.
    """

    current_page: int
    page_quantity: int
    docs_quantity: int
    docs: list
