# <center>Primeiros passos</center>

Neste guia, orientaremos você nas etapas iniciais para começar a usar o **PyODMongo**, um Mapeador de Objetos-Documentos (ODM) do MongoDB em Python. Abordaremos a criação de um motor, a definição de um modelo, o salvamento de dados e a leitura do banco de dados.

## Criando o motor

Para começar a usar o **PyODMongo**, primeiro você precisa criar uma instância da classe `AsyncDbEngine` ou `DbEngine` para se conectar ao seu servidor MongoDB. Veja como você pode fazer isso:

/// tab | Async
```python hl_lines="5"
from pyodmongo import AsyncDbEngine, DbModel
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
    result = await engine.save(box)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="4"
from pyodmongo import DbEngine, DbModel
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)

result = engine.save(box)
```
///

Certifique-se de substituir `mongodb://localhost:27017` pela string de conexão com seu banco de dados do MongoDB e `my_db` pelo nome do banco.

## Definindo um modelo
A seguir, você definirá um modelo que herda de DbModel. Este modelo representa a estrutura dos seus documentos MongoDB. Você também precisará criar o atributo `_collection`, que carregará a string do nome da coleção a ser salva no banco de dados.

/// tab | Async
```python hl_lines="8 12"
from pyodmongo import AsyncDbEngine, DbModel
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
    result = await engine.save(box)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="7 11"
from pyodmongo import DbEngine, DbModel
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)

result = engine.save(box)
```
///

Neste exemplo, criamos uma classe `Product`, que herda de `DbModel`, para definir a estrutura de nossos documentos no MongoDB.

## Salvando dados
Você pode salvar dados no MongoDB usando o método `save()` da sua instância `AsyncDbEngine` ou `DbEngine`.

/// tab | Async
```python hl_lines="19"
from pyodmongo import AsyncDbEngine, DbModel
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
    result = await engine.save(box)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="16"
from pyodmongo import DbEngine, DbModel
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


box = Product(name='Box', price='5.99', is_available=True)

result = engine.save(box)
```
///

Este código cria um novo documento usando os dados fornecidos e salva no MongoDB.

## Lendo do banco de dados
Para ler dados do banco de dados, você pode usar o método `find_one()` da sua instância `AsyncDbEngine` ou `DbEngine`.

/// tab | Async
```python hl_lines="18"
from pyodmongo import AsyncDbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


async def main():
    query = eq(Product.name, 'Box')
    box: Product = await engine.find_one(Model=Product, query=query)

asyncio.run(main())
```
///

/// tab | Sync
```python hl_lines="16"
from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


query = eq(Product.name, 'Box')
box: Product = engine.find_one(Model=Product, query=query)
```
///

Este código consulta o banco de dados em busca de um produto com o nome 'Box' e cria um objeto do tipo `Product` com o documento encontrado no banco de dados.

Estes são os primeiros passos para você começar a usar o **PyODMongo**. Agora você pode criar, salvar e ler dados de seu banco de dados MongoDB usando este Mapeador de Objetos-Documentos MongoDB em Python.