# <center>Getting Started</center>


In this guide, we'll walk you through the initial steps to get started with **PyODMongo**, a Python MongoDB Object-Document Mapper (ODM). We'll cover creating the engine, defining a model, saving data, and reading from the database.

## Creating Engine

To begin using **PyODMongo**, you first need to create an instance of the `AsyncDbEngine` or `DbEngine` class to connect to your MongoDB server. Here's how you can do it:

/// tab | Async
```python hl_lines="5"
__save_async.py__
```
///

/// tab | Sync
```python hl_lines="4"
__save_sync.py__
```
///

Make sure to replace `mongodb://localhost:27017` with the connection string to your MongoDB database and `my_db` with database name.

!!! tip
    When creating an engine, you can pass the `tz_info` parameter in the `AsyncDbEngine` or `DbEngine` classes which sets the default time zone for all `find_one` and `find_many` operations performed through this engine, unless `tz_info ` is also passed in the `find_one` and `find_many` methods. In this case, the time zone of the search methods will prevail.

## Defining a Model
Next, you'll define a model that inherits from DbModel. This model represents the structure of your MongoDB documents. You'll also need to create the `_collection` attribute, which will carry the collection name string to be saved in the database.

/// tab | Async
```python hl_lines="8 12"
__save_async.py__
```
///

/// tab | Sync
```python hl_lines="7 11"
__save_sync.py__
```
///

In this example, we've created a `Product` class, that inherits from `DbModel`, to define the structure of our MongoDB documents.

## Saving Data
You can save data to the MongoDB database using the `save()` method of your `AsyncDbEngine` or `DbEngine` instance.

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

This code creates a new document using the data provided, and then it is saved to the MongoDB database.

## Reading from the Database
To read data from the database, you can use the `find_one()` method of your `AsyncDbEngine` or `DbEngine` instance.

/// tab | Async
```python hl_lines="17"
__find_one_async.py__
```
///

/// tab | Sync
```python hl_lines="15"
__find_one_sync.py__
```
///

This code queries the database for a product with name 'Box' and creates a `Product` type object with the document found in database.

These are the first steps to get you started with **PyODMongo**. You can now create, save, and read data from your MongoDB database using this Python MongoDB Object-Document Mapper.