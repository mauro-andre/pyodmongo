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


**PyODMongo** is a modern Python library that functions as a robust Object-Document Mapper (ODM) for **MongoDB**. Leveraging the power of **Pydantic V2**, it seamlessly bridges the gap between Python and MongoDB, offering an intuitive and efficient way to interact with MongoDB documents.

By using **PyODMongo**, you can effortlessly map your Python classes to MongoDB documents, allowing for a more Pythonic approach to handling data. This library simplifies the entire process of defining and working with MongoDB collections, documents, and queries.

**PyODMongo** is built on top of **Pydantic V2**, making the `DbModel` class an extension of Pydantic's `BaseModel`. This means that all the rich functionality of Pydantic's `BaseModel`, including **Validators**, **Fields** and **Model Config**, is readily available in `DbModel`.

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

Contributions to **PyODMongo** are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/mauro-andre/pyodmongo).

## License
**PyODMongo** is licensed under the MIT License. See the [LICENSE file](https://github.com/mauro-andre/pyodmongo/blob/master/LICENSE) for more information.