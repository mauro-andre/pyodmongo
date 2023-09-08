# <center>Overview</center>

![Image title](./assets/images/pyodmongo_Logo_BG_Dark.png#only-dark)
![Image title](./assets/images/pyodmongo_Logo_BG_White.png#only-light)

<div align="center">
    <a href="https://pypi.org/project/pyodmongo/" target="_blank">
      <img src="https://img.shields.io/pypi/v/pyodmongo" alt="coverage">
    </a>
    <a href="https://pypi.org/project/pyodmongo/" target="_blank">
      <img src="https://img.shields.io/badge/Python-3.11-green" alt="pre-commit">
    </a>
</div>


`pyodmongo` is a Python library that serves as an Object-Document Mapper (ODM) for MongoDB. It is built on top of the popular `pydantic V2` library, making it easy to work with MongoDB documents in a Pythonic and efficient way.

With `pyodmongo`, you can seamlessly map your Python classes to MongoDB documents, allowing you to work with data in a more intuitive and Pythonic manner. It simplifies the process of defining and interacting with MongoDB collections, documents, and queries.

## Key Features

- **Integration with pydantic**: Leverage the power of pydantic's data validation and modeling capabilities while working with MongoDB data.

- **Automatic Schema Generation**: Define your MongoDB schema using pydantic models, and `pyodmongo` will automatically create the necessary MongoDB collections and ensure data consistency.

- **Query Builder**: Easily construct complex MongoDB queries using Python code, reducing the need for writing raw query strings.

- **Document Serialization**: Serialize and deserialize Python objects to and from MongoDB documents effortlessly.

- **Async Support**: Take advantage of asynchronous programming with `pyodmongo` to enhance the performance of your MongoDB operations.

- **Active Development**: `pyodmongo` is actively developed and maintained, with new features and improvements being regularly added.

## Installation

You can install `pyodmongo` using pip:

```bash
pip install pyodmongo
```

## Contributing

Contributions to `pyodmongo` are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/mauro-andre/pyodmongo).

## License
`pyodmongo` is licensed under the MIT License. See the [LICENSE file](https://github.com/mauro-andre/pyodmongo/blob/master/LICENSE) for more information.