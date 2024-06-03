# <center>DbModel</center>

In **PyODMongo**, the `DbModel` class serves as the foundational element for modeling MongoDB collections. When you create a class that inherits from `DbModel`, it automatically becomes a representation of a MongoDB collection.

Thanks to the **PyODMongo** and Pydantic integration, you can create MongoDB collections and define their schema effortlessly, combining the strengths of MongoDB with the convenience of Pydantic classes and their data validation.

```python
__db_model.py__
```

To ensure that your Python class is correctly mapped to the corresponding MongoDB collection, it's essential to include the `_collection` attribute. This attribute should be a `ClassVar` with a string value containing the desired name of the collection in your MongoDB database.

## DbModel Inherited Attributes

When you create a class that inherits from `DbModel`, it not only represents a MongoDB collection but also inherits some additional attributes automatically. These inherited attributes provide essential metadata for your documents and are created automatically if not explicitly provided when instantiating objects.

### `id: Id`

Each document derived from DbModel inherits an id attribute, represented by the `Id` class. This attribute serves as a unique identifier for the document within its MongoDB collection. If you don't specify an id when creating a new instance, one will be generated automatically.

!!! note "Id Class"
    Under the hood, **PyODMongo** processes instances of the `Id` class to be stored as `ObjectId` in MongoDB. This transformation is handled transparently, so you can interact with `Id` instances as if they were regular strings in your Python code. You also have the flexibility to input either a `str` or an `ObjectId`, **PyODMongo** will handle the conversion.

!!! tip
    The `id` attribute is the same as `_id` in MongoDb.

### `created_at: datetime`

The `created_at` attribute in **PyODMongo** is a timestamp that is entirely managed by the **PyODMongo** library. It serves as a record of when a document was initially created in the database. This attribute is automatically generated at the moment of document creation.

### `updated_at: datetime`

Similarly, the `updated_at` attribute in **PyODMongo** is another timestamp that is fully managed by the **PyODMongo** library. It serves as an indicator of when a document was last modified in the database. This field is automatically updated whenever changes are made to the document.

## Relationships

In **PyODMongo**, you can model relationships between documents using references and embedded documents. These relationships allow you to represent complex data structures and associations in your MongoDB database.

### Reference Relationships

Reference relationships involve referencing one document from another using an identifier. In **PyODMongo**, you can establish reference relationships between documents by including fields that store references to other documents' identifiers.

```python hl_lines="15"
__reference.py__
```

In this case **PyODMongo** will accept `user` can be an instance of `User` or an `Id` reference

!!! tip
    You can also have a list of references including `user: list[User | Id]`

### Embedded Documents

Embedded documents involve nesting one document within another. In **PyODMongo**, you can define embedded relationships by including fields that represent nested documents.

/// tab | PyODMongo MainBaseModel
```python hl_lines="5"
__embedded_mainbasemodel.py__
```
///
/// tab | Pydantic BaseModel
```python hl_lines="6"
__embedded_basemodel.py__
```
///

!!! note
    The difference between using `MainBaseModel` and `BaseModel` is that some search methods, such as the `$elemMatch` operator, require `MainBaseModel` for nested elements. Therefore, it is always recommended to use `MainBaseModel`.

!!! tip
    You can also embed documents from other `DbModel` objects instead of `BaseModel`. This is great when you want to keep current information in a document.

### Leveraging Relationships

By modeling relationships in **PyODMongo**, you can create more complex and structured data schemas, enabling you to build sophisticated applications that capture real-world data associations. Whether it's reference relationships for linking documents or embedded relationships for nesting documents, **PyODMongo** provides the flexibility to design your data models according to your application's needs.