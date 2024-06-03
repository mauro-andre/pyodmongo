# <center>Query Operators</center>

Creating queries in **PyODMongo** is straightforward and intuitive. It simplifies the process of building MongoDB queries, providing a Pythonic and straightforward approach.

In **PyODMongo**, a query serves as an essential attribute of the `find_many`, `find_one`, `delete` and `save` methods, which are available through the `DbEngine` and `AsyncDbEngine` classes. These methods empower you to retrieve data from your MongoDB database with ease, combining the simplicity of Python with the robust querying capabilities of MongoDB.

## Operators

### Equal
The **Equal** operator is used to match documents where the value of a field is equal to the specified value. It's a basic comparison operator in MongoDB and **PyODMongo**.

/// tab | Magic method
```python hl_lines="14"
__eq_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__eq_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{name: {$eq: "Box"}}
```

### Grater than
The **Greater than** operator is used to match documents where the value of a field is greater than the specified value. It helps in filtering out records that exceed a certain threshold.

/// tab | Magic method
```python hl_lines="14"
__gt_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__gt_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{price: {$gt: 10}}
```

### Grater than equal
The **Greater than equal** operator matches documents where the value of a field is greater than or equal to the specified value. This is useful for range queries including the boundary value.

/// tab | Magic method
```python hl_lines="14"
__gte_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__gte_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{price: {$gte: 10}}
```

### In
The **In** operator allows you to specify an array of possible values for a field. It matches documents where the field’s value is in the specified array.

/// tab | PyODMongo queries
```python hl_lines="3 15"
__in_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{name: {$in: ["Ball", "Box", "Toy"]}}
```

### Lower than
The **Lower than** operator matches documents where the value of a field is less than the specified value. This is used for filtering records below a certain threshold.

/// tab | Magic method
```python hl_lines="14"
__lt_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__lt_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{price: {$lt: 10}}
```

### Lower than equal
The **Lower than equal** operator matches documents where the value of a field is less than or equal to the specified value. This includes the boundary value in the results.

/// tab | Magic method
```python hl_lines="14"
__lte_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__lte_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{price: {$lte: 10}}
```

### Not equal
The **Not equal** operator matches documents where the value of a field is not equal to the specified value. It is used to exclude documents with a specific value.

/// tab | Magic method
```python hl_lines="14"
__ne_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__ne_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{name: {$ne: "Box"}}
```

### Not in
The **Not** in operator allows you to specify an array of values that the field should not be equal to. It matches documents where the field’s value is not in the specified array.

/// tab | PyODMongo queries
```python hl_lines="3 15"
__nin_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{name: {$nin: ["Ball", "Box", "Toy"]}}
```

### And
The **And** operator is used to join multiple query clauses with a logical **AND**. It ensures that all specified conditions must be true for a document to be included in the result set.

/// tab | Magic method
```python hl_lines="14"
__and_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__and_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{$and: [{price: {$gt: 10}}, {price: {$lte: 50}}]}
```

### Or
The **Or** operator joins query clauses with a logical **OR**, matching documents that satisfy at least one of the specified conditions.

/// tab | Magic method
```python hl_lines="14"
__or_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__or_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{$or: [{name: {$eq: "Box"}}, {price: {$eq: 100}}]}
```

### Nor
The **Nor** operator joins query clauses with a logical NOR, matching documents that fail all of the specified conditions.

/// tab | PyODMongo queries
```python hl_lines="3 15"
__nor_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{$nor: [{name: {$eq: "Box"}}, {price: {$eq: 100}}]}
```

### Elem match
The **Elem match** operator is used to match documents that contain an array field with at least one element that matches all the specified criteria.

/// tab | PyODMongo queries
```python hl_lines="3 20"
__elem_match_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{$products: {$elemMatch: {name: "Box", price: 50}}}
```

### Sort
The **Sort** operator arranges the results of a query in a specified order. It is useful for organizing data either in ascending or descending order based on a particular field.

/// tab | PyODMongo queries
```python hl_lines="3 16"
__sort_pyodmongo_queries.py__
```
///

Equivalent filter in MongoDB
```javascript
{name: 1, price: -1}
```
