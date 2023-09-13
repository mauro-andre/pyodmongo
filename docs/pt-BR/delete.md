# <center>Delete</center>

## Delete

O método `delete` está disponível em `AsyncDbEngine` e `DbEngine` e é usado para excluir documentos de uma coleção MongoDB com base em uma consulta especificada. Este método oferece uma maneira direta de remover documentos que atendem à consulta especificada do seu banco de dados MongoDB.

/// tab | Async
```python hl_lines="21"
from pyodmongo import AsyncDbEngine, DbModel, DeleteResponse
from pyodmongo.queries import eq
from typing import ClassVar
import asyncio

# Initialize the database engine
engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

# Define a model
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

async def main():
    # Define a query to specify which documents to delete
    query = eq(Product.name, 'Box')

    # Use the delete method to remove documents
    result: DeleteResponse = await engine.delete(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="19"
from pyodmongo import DbEngine, DbModel, DeleteResponse
from pyodmongo.queries import eq
from typing import ClassVar

# Initialize the database engine
engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

# Define a model
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

# Define a query to specify which documents to delete
query = eq(Product.name, 'Box')

# Use the delete method to remove documents
result: DeleteResponse = engine.delete(Model=Product, query=query)
```
///

### Argumentos

- `Model: type[DbModel]`: A classe que herda de `DbModel` e serve de base para consulta ao banco de dados.
- `query: ComparisonOperator | LogicalOperator`: Consulta que define os critérios de seleção dos documentos a serem excluídos.
- `raw_query: dict (opcional)`: Uma consulta bruta em formato de dicionário aceita pelo MongoDB.

!!! warning
    Nos bastidores, o método `delete` usa a operação `delete_many` do MongoDB para remover documentos. Todos os documentos que correspondam aos critérios de consulta serão excluídos da coleção.


## Delete one

O método `delete_one` é semelhante ao método `delete`, a principal diferença é que ele excluirá apenas o primeiro documento que corresponder à consulta especificada.

/// tab | Async
```python
from pyodmongo import AsyncDbEngine, DeleteResponse

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')
result: DeleteResponse = async engine.delete_one(Model=Product, query=query)
```
///
/// tab | Sync
```python
from pyodmongo import DbEngine, DeleteResponse

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')
result: DeleteResponse = engine.delete_one(Model=Product, query=query)
```
///

## Delete Response

O `DeleteResponse` é o objeto de retorno para os métodos `delete` e `delete_one`, fornecendo informações sobre o resultado da operação de exclusão.

### Atributos

- `acknowledged: bool`: Indica se a operação de exclusão foi reconhecida pelo servidor MongoDB. Se `True`, significa que o servidor reconheceu a operação; caso contrário, é `False`.
- `deleted_count: int`: Representa a quantidade de documentos que foram excluídos com sucesso pela operação. Essa contagem pode variar dependendo dos critérios de consulta.
- `raw_result: dict`: Um dicionário contendo o resultado bruto da operação de exclusão retornado pelo driver MongoDB. Ele fornece detalhes adicionais sobre o resultado da operação.