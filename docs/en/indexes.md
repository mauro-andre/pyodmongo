# <center>Indexes</center>

Indexes play a crucial role in optimizing database performance, and **PyODMongo** provides you with flexible options for defining and managing them. This section will guide you on how to create indexes using PyODMongo.

## Simple Index Creation

The simplest way to create indexes in **PyODMongo** is by using the `Field`, specifying which field should be indexed.

```python
__indexes.py__
```

- `index: bool`: When set to `True`, this Field will result in the creation of an index in the MongoDB collection using the same name as the field.
- `unique: bool`: When set to `True`, this Field enforces uniqueness for the indexed values in the MongoDB collection. In other words, no two documents in the collection can have the same value for this field.
- `text_index: bool`: Setting this Field to `True` indicates that the field should be included in the text indexes of the MongoDB collection. Text indexes are used for full-text search functionality.
- `default_language: str`: The default language that MongoDb will set in collection text index. You can check more detail in <a href="https://www.mongodb.com/docs/manual/reference/text-search-languages/#std-label-text-search-languages" target="_blank">Text Search Languages</a>.

## Advanced Index Creation

However, if you need to create more specific or complex indexes, you can utilize the `IndexModel` from PyMongo. To do this, define a class-level attribute `_indexes` as a list of `IndexModel` instances. You can find detailed information about creating indexes with PyMongo in their <a href="https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_indexes" target="_blank">official documentation</a>.

Here's an example of how to create custom indexes in PyODMongo:

```python
__indexes_advanced.py__
```

In this example, we define two custom indexes for the `Product` model using `IndexModel`. The first index is a compound index on the `name` field in ascending order and the `price` field in descending order, named 'name_and_price'. The second index is on the `product_type` field in descending order, named 'product_type'.

PyODMongo supports creating any index structure by following the PyMongo index structure guidelines. This flexibility allows you to optimize your database performance according to your specific requirements.