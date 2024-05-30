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
    <a href="/coverage" target="_blank">
      <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fs3.amazonaws.com%2Fpyodmongo.dev%2Fcoverage%2Fcoverage_badge.json&logo=pytest" alt="pre-commit">
    </a>
    <a href="https://pepy.tech/project/pyodmongo" target="_blank">
      <img src="https://static.pepy.tech/badge/pyodmongo/month">
    </a>
</div>

**PyODMongo** is a modern Python library that serves as a robust Object-Document Mapper (ODM) and seamlessly bridges the gap between Python and **MongoDB**. It offers an intuitive and efficient way to interact with documents.

Built on top of **Pydantic V2**, **PyODMongo** ensures that documents in the database rigorously represent the structure of Python objects. This means that documents are saved and retrieved from the database exactly as a Python object is structured, regardless of how nested the objects are and whether they are stored persistently or by reference. **PyODMongo** can automatically populate these documents.

## Key Features

- **Integration with pydantic**: Leverage the power of pydantic's data validation and modeling capabilities while working with MongoDB data.

- **Automatic Schema Generation**: Define your MongoDB schema using pydantic models, and **PyODMongo** will automatically create the necessary MongoDB collections and ensure data consistency.

- **Query Builder**: Easily construct complex MongoDB queries using Python code, reducing the need for writing raw query strings.

- **Document Serialization**: Serialize and deserialize Python objects to and from MongoDB documents effortlessly.

- **Async Support**: Take advantage of asynchronous programming with **PyODMongo** to enhance the performance of your MongoDB operations.

- **Active Development**: **PyODMongo** is actively developed and maintained, with new features and improvements being regularly added.

## Installation

You can install **PyODMongo** using pip:

```bash
pip install pyodmongo
```

## Contributing

Contributions to **PyODMongo** are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request on the <a href="https://github.com/mauro-andre/pyodmongo" target="_blank">GitHub repository</a>.

## License
**PyODMongo** is licensed under the MIT License. See the <a href="https://github.com/mauro-andre/pyodmongo/blob/master/LICENSE" target="_blank">LICENSE file</a> for more information.