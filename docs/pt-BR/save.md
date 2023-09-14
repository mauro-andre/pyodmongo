# <center>Save</center>

## Save

O método `save` faz parte das classes `AsyncDbEngine` e `DbEngine` no **PyODMongo**. É responsável por salvar ou atualizar documentos no banco de dados.

/// tab | Async
```python hl_lines="19"
from pyodmongo import AsyncDbEngine, DbModel, SaveResponse
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)


async def main():
    result: SaveResponse = await engine.save(box)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="16"
from pyodmongo import DbEngine, DbModel, SaveResponse
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)

result: SaveResponse = engine.save(box)
```
///

Se o resultado do método `save` corresponder à criação de um novo documento no banco de dados, a instância do objeto receberá os atributos `id`, `created_at` e `updated_at`.

## Argumentos

- `obj: Any`: Objeto a ser salvo no banco de dados.
- `query: ComparisonOperator | LogicalOperator = None`: Consulta usada para atualizar documentos correspondentes. Caso não seja fornecido, o documento no banco de dados com `_id` igual a `obj.id` será atualizado. Se `obj` não tiver um `id`, um novo documento será criado no banco de dados.
- `raw_query: dict = None`: Consulta no formato aceito pelo MongoDB. Este parâmetro permite especificar uma consulta personalizada para atualização de documentos.

!!! warning
    Se `raw_query` for passado, `query` não será considerado.

!!! note
    Por trás dos panos, o **PyODMongo** usa a operação `update_many` com `upsert=True`, o que significa que ele pode adicionar ou atualizar um ou vários documentos.


## Save all

Além do método `save`, **PyODMongo** fornece o método `save_all`, que permite salvar uma lista de objetos. Este método é particularmente útil quando você precisa salvar vários documentos.

/// tab | Async
```python hl_lines="22"
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


class User(DbModel):
    name: str
    email: str
    password: str
    _collection: ClassVar = 'users'


obj_list = [
    Product(name='Box', price='5.99', is_available=True),
    Product(name='Ball', price='6.99', is_available=True),
    User(name='John', email='john@email.com', password='john_pwd')
]

async def main():
    result: list[SaveResponse] = await engine.save_all(obj_list)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="21"
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


class User(DbModel):
    name: str
    email: str
    password: str
    _collection: ClassVar = 'users'


obj_list = [
    Product(name='Box', price='5.99', is_available=True),
    Product(name='Ball', price='6.99', is_available=True),
    User(name='John', email='john@email.com', password='john_pwd')
]

result: list[SaveResponse] = engine.save_all(obj_list)
```
///

## Save response

O método `save` no **PyODMongo** retorna um objeto `SaveResponse` que fornece informações sobre o resultado da operação de salvamento. Este objeto contém vários atributos que fornecem informações sobre como a operação de salvamento afetou o banco de dados.

### Atributos

- `acknowledged`: Um valor booleano que indica se a operação foi reconhecida pelo servidor MongoDB. Se a operação foi confirmada, este atributo é definido como `True`, indicando que o servidor reconheceu e processou o pedido de salvamento.

- `matched_count`: Um inteiro que representa o número de documentos no banco de dados que corresponderam à consulta ou aos critérios especificados durante a operação de salvamento. Esta contagem indica quantos documentos existentes foram atualizados.

- `modified_count`: Um inteiro que representa o número de documentos no banco de dados que foram realmente modificados durante a operação de salvamento. Essa contagem geralmente é igual a `matched_count` ou a um subconjunto dele e indica quantos documentos tiveram seus campos alterados.

- `upserted_id`: Se a operação de salvamento resultou na inserção de um novo documento (upsert), este atributo contém o `_id` do documento recém-inserido. Quando nenhum upsert ocorre, este atributo é `None`.

- `raw_result`: Um dicionário contendo o resultado bruto da operação de salvamento do MongoDB. Este dicionário pode conter informações adicionais fornecidas pelo servidor MongoDB e sua estrutura pode variar de acordo com o driver e a versão específicos do MongoDB.