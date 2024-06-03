# <center>Save</center>

## Save

The `save` method is a part of the `AsyncDbEngine` and `DbEngine` classes in **PyODMongo**. It is responsible for saving or updating documents in the database.

/// tab | Async
```python hl_lines="19"
__save_async.py__
```
///

/// tab | Sync
```python hl_lines="16"
__save_sync.py__
```
///

If the result of the `save` method corresponds to the creation of a new document in the database, the object instance will receive the `id`, `created_at`, and `updated_at` attributes.

## Arguments

- `obj: Any`: The object to be saved in the database.
- `query: ComparisonOperator | LogicalOperator = None`: A query used to update matching documents. If not provided, the document in the database with `_id` equals to `obj.id` will be updated. If `obj` does not have an `id`, a new document will be created in the database.
- `raw_query: dict = None`: A query in the format accepted by MongoDB. This parameter allows you to specify a custom query for updating documents.

!!! warning
    If `query` is passed, `raw_query` will not be considered.

!!! note
    Under the hood, **PyODMongo** uses the `update_many` operation with `upsert=True`, which means it can add or update one or multiple documents.


## Save all

In addition to the `save` method, **PyODMongo** provides the `save_all` method, which enables you to save a list of objects. This method is particularly useful when you need to save multiple documents.

/// tab | Async
```python hl_lines="30"
__save_all_async.py__
```
///
/// tab | Sync
```python hl_lines="28"
__save_all_sync.py__
```
///

## Save responses

The `save` method in **PyODMongo** returns a `DbResponse` object that provides information about the outcome of the save operation. This object contains several attributes that give insights into how the save operation affected the database.

The return value of a `save_all` method is a dictionary where the keys are the names of the collections and the values are `DbResponse` objects.

### `DbResponse` Attributes

- `acknowledged: bool`: A boolean value indicating whether the operation was acknowledged by the MongoDB server. If the operation was acknowledged, this attribute is set to `True`, indicating that the server recognized and processed the save request.

- `deleted_count: int`: An integer representing the number of documents that were deleted from the database as part of the delete operation.

- `inserted_count: int`: An integer that indicates the number of documents that were successfully inserted into the database during the insert operation.

- `matched_count: int`: An integer that represents the number of documents in the database that matched the query or criteria specified during the save operation. This count indicates how many existing documents were updated as part of the save operation.

- `modified_count: int`: An integer that represents the number of documents in the database that were actually modified during the save operation. This count is usually the same as or a subset of the `matched_count` and indicates how many documents had their fields changed.

- `upserted_count: int`: An integer that represents the number of documents that were inserted as a result of an upsert operation. This occurs when a document does not exist and is created during the update process.

- `upserted_ids: dict[int, Id]`: A dictionary that maps the index of the upserted documents to their new unique IDs. This attribute is useful for tracking which documents were created during an upsert operation.
