# <center>Delete</center>

## Delete

The `delete` method is available in both `AsyncDbEngine` and `DbEngine` and is used to delete documents from a MongoDB collection based on a specified query. This method offers a straightforward way to remove documents that match specific criteria from your MongoDB database.

/// tab | Async
```python hl_lines="18"
__delete_async.py__
```
///
/// tab | Sync
```python hl_lines="16"
__delete_sync.py__
```
///

### Arguments

- `Model: DbModel`: The class that inherits from `DbModel` and serves as the base for querying the database.
- `query: ComparisonOperator | LogicalOperator`: A query that defines the criteria for selecting the documents to be deleted.
- `raw_query: dict (optional)`: A raw query in dictionary format accepted by MongoDB.

!!! warning
    Under the hood, the `delete` method uses MongoDB's `delete_many` operation to remove documents. All documents that match the query criteria will be deleted from the collection.


## Delete one

In **PyODMongo**, there is only the `delete` method. To ensure that only one document is deleted, you can pass the attribute `delete_one=True` to the `delete` method. This way, only the first document that matches the specified query will be deleted.

/// tab | Async
```python hl_lines="18-20"
__delete_one_async.py__
```
///
/// tab | Sync
```python hl_lines="16"
__delete_one_sync.py__
```
///

## Delete Response
The `delete` method in **PyODMongo** returns a `DbResponse` object that provides information about the outcome of the delete operation. This object contains several attributes that give insights into how the delete operation affected the database.

### Atributos de `DbResponse`

- `acknowledged: bool`: A boolean value indicating whether the operation was acknowledged by the MongoDB server. If the operation was acknowledged, this attribute is set to `True`, indicating that the server recognized and processed the save request.

- `deleted_count: int`: An integer representing the number of documents that were deleted from the database as part of the delete operation.

- `inserted_count: int`: An integer that indicates the number of documents that were successfully inserted into the database during the insert operation.

- `matched_count: int`: An integer that represents the number of documents in the database that matched the query or criteria specified during the save operation. This count indicates how many existing documents were updated as part of the save operation.

- `modified_count: int`: An integer that represents the number of documents in the database that were actually modified during the save operation. This count is usually the same as or a subset of the `matched_count` and indicates how many documents had their fields changed.

- `upserted_count: int`: An integer that represents the number of documents that were inserted as a result of an upsert operation. This occurs when a document does not exist and is created during the update process.

- `upserted_ids: dict[int, Id]`: A dictionary that maps the index of the upserted documents to their new unique IDs. This attribute is useful for tracking which documents were created during an upsert operation.