# <center>Fields</center>

In **PyODMongo**, `Fields` serve as an extension of Pydantic Fields, offering the same rich set of functionalities while introducing three additional arguments for fine-tuned control over MongoDB index creation within your collections.

```python
from pyodmongo import DbModel, Field
from typing import ClassVar


class User(DbModel):
    name: str = Field(index=True, text_index=True)
    email: str = Field(index=True, unique=True)
    password: str
    is_active: bool
    _collection: ClassVar = 'users'
```

- `index: bool`: When set to `True`, this Field will result in the creation of an index in the MongoDB collection using the same name as the field.
- `unique: bool`: When set to `True`, this Field enforces uniqueness for the indexed values in the MongoDB collection. In other words, no two documents in the collection can have the same value for this field.
- `text_index: bool`: Setting this Field to `True` indicates that the field should be included in the text indexes of the MongoDB collection. Text indexes are used for full-text search functionality.
- `default_language: str`: The default language that MongoDb will set in collection text index. You can check more detail in <a href="https://www.mongodb.com/docs/manual/reference/text-search-languages/#std-label-text-search-languages" target="_blank">Text Search Languages</a>.

For a comprehensive understanding of the base Field features, you can refer to the <a href="https://docs.pydantic.dev/latest/api/fields/" target="_blank">Pydantic Fields documentation</a>.