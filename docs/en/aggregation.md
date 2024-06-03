# <center>Aggregation</center>

Aggregation is a fantastic feature of MongoDB that allows you to perform various data transformations and analysis. Although MongoDB's Aggregation Pipeline is a powerful tool, it can sometimes be complex to work with due to its stages and expressions, but once you master the tool, it becomes a powerful ally in data analysis.

At **PyODMongo**, we offer you the ability to leverage the full power of the MongoDB aggregation framework and to use it you need to be familiar with this feature.

To utilize the capabilities of aggregation in **PyODMongo**, you can insert aggregation pipelines directly into your models. All you need to do is create a class-level attribute named `_pipeline` in your model and defining the aggregation stages. When you use the `find_one` or `find_many` methods in **PyODMongo**, the library will execute the aggregation pipeline and return the result as Python objects.

Here's a simple example using just the `$group` stage from the MongoDB Aggregation Pipeline:

/// tab | Async
```python
__aggregation_async.py__
```
///
/// tab | Sync
```python
__aggregation_sync.py__
```
///

!!! tip
    PyODMongo already uses aggregation in the `find` and `find_one` methods under the hood. The `query` parameter in these methods is actually converted into a `$match` stage and inserted as the first stage of the aggregation pipeline. You can continue using this combination by passing `query` parameter in `find` and `find_one` methods and `_pipeline` in your class.

In this example, we have an `OrdersByCustomers` model with an aggregation pipeline that groups orders by customer, calculating the count of orders and the total order value for each customer.

**PyODMongo** provides flexibility in using aggregation, but it's essential to ensure that the aggregation output aligns with the fields defined in your class to avoid errors when instantiating objects.

With PyODMongo's aggregation support, you can unlock the full potential of MongoDB's data transformation capabilities while maintaining a Pythonic and intuitive coding experience. The possibilities for data analysis and processing are virtually limitless.