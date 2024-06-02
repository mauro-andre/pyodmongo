# <center>Query Operators</center>

Creating queries in **PyODMongo** is straightforward and intuitive. It simplifies the process of building MongoDB queries, providing a Pythonic and straightforward approach.

In **PyODMongo**, a query serves as an essential attribute of the `find_many`, `find_one`, `delete` and `save` methods, which are available through the `DbEngine` and `AsyncDbEngine` classes. These methods empower you to retrieve data from your MongoDB database with ease, combining the simplicity of Python with the robust querying capabilities of MongoDB.

## Operators

### Equal

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

### Grater than

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

### Grater than equal

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

### In

/// tab | PyODMongo queries
```python hl_lines="3 15"
__in_pyodmongo_queries.py__
```
///

### Lower than

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

### Lower than equal

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

### Not equal

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

### Not in

/// tab | PyODMongo queries
```python hl_lines="3 15"
__nin_pyodmongo_queries.py__
```
///

### And

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

### Or

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

### Nor

/// tab | PyODMongo queries
```python hl_lines="3 15"
__nor_pyodmongo_queries.py__
```
///

### Elem match

/// tab | PyODMongo queries
```python hl_lines="3 20"
__elem_match_pyodmongo_queries.py__
```
///

### Sort

/// tab | PyODMongo queries
```python hl_lines="3 16"
__sort_pyodmongo_queries.py__
```
///
