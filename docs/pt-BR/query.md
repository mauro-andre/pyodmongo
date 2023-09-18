# <center>Query</center>

Criar consultas no **PyODMongo** é simples e intuitivo. Ele simplifica o processo de criação de consultas do MongoDB, fornecendo uma abordagem Pythônica e direta para trabalhar com **Operadores de comparação** e **Operadores lógicos** encontrados no MongoDB.

No **PyODMongo**, uma consulta serve como um atributo essencial dos métodos `find_many` e `find_one`, que estão disponíveis através das classes `DbEngine` e `AsyncDbEngine`. Esses métodos permitem recuperar dados do seu banco de dados MongoDB com facilidade, combinando a simplicidade do Python com os recursos robustos de consulta do MongoDB.

## Operadores de comparação

| Operador | Descrição |
| ---------| ------------------------------------ |
| `eq` | Corresponde a valores iguais a um valor especificado. |
| `gt` | Corresponde a valores maiores que um valor especificado. |
| `gte` | Corresponde a valores maiores ou iguais a um valor especificado. |
| `in_` | Corresponde a qualquer um dos valores especificados em uma lista. |
| `lt` | Corresponde a valores menores que um valor especificado. |
| `lte` | Corresponde a valores menores ou iguais a um valor especificado. |
| `ne` | Corresponde a todos os valores que não são iguais a um valor especificado. |
| `nin` | Corresponde a qualquer valor que não esteja na lista. |


Ao usar esses operadores de comparação no PyODMongo, você normalmente fornecerá dois argumentos:

- `field: DbField`: Este argumento representa o campo da sua classe `DbModel` do PyODMongo que você deseja pesquisar no banco de dados. Ele define a propriedade à qual você deseja aplicar o operador de comparação.

- `value: Any`: Este argumento especifica o valor que você deseja comparar com o campo definido no primeiro argumento. Representa o valor de referência a ser encontrado no banco de dados.

Aqui está um exemplo de como usar um operador de comparação no PyODMongo:

/// tab | Async
```python hl_lines="18"
from pyodmongo import AsyncDbEngine, DbModel
from pyodmongo.queries import ( eq, gt, gte, in_, lt, lte, ne, nin, text, 
                                and_, or_, nor)
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


async def main():
    query = gte(Product.price, 5)
    result: Product = await engine.find_one(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="16"
from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import ( eq, gt, gte, in_, lt, lte, ne, nin, text, 
                                and_, or_, nor)
from typing import ClassVar

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


query = gte(Product.price, 5)
result: Product = engine.find_one(Model=Product, query=query)
```
///

Neste exemplo, a consulta retornará todos os documentos da collection 'products' onde o campo price for igual ou superior a 5.

## Operadores lógicos

Assim como os operadores de comparação, os operadores lógicos no **PyODMongo** são projetados para espelhar seus equivalentes no próprio MongoDB.

Aqui estão os principais operadores lógicos disponíveis no PyODMongo:

| Operador | Descrição |
| ---------| ------------------------------------ |
| `and_` | Unir cláusulas de consulta com um **AND** lógico. Retorna todos os documentos que correspondem às condições de todas as cláusulas. |
| `or_` | Unir cláusulas de consulta com um **OR** lógico. Retorna todos os documentos que correspondem às condições de qualquer uma das cláusulas. |
| `nor` | Unir cláusulas de consulta com um **NOR** lógico. Retorna o inverso do **OR** |


Aqui está um exemplo de como você pode usar operadores lógicos no PyODMongo:

/// tab | Async
```python hl_lines="18"
from pyodmongo import AsyncDbEngine, DbModel
from pyodmongo.queries import (eq, gt, gte, in_, lt, lte, ne, nin, text,
                               and_, or_, nor)
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


async def main():
    query = and_(
        eq(Product.is_available, True),
        gte(Product.price, 5)
    )
    result: Product = await engine.find_one(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="17"
from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import (eq, gt, gte, in_, lt, lte, ne, nin, text,
                               and_, or_, nor)
from typing import ClassVar
import asyncio

engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


query = and_(
    eq(Product.is_available, True),
    gte(Product.price, 5)
)
result: Product = engine.find_one(Model=Product, query=query)

```
///

Neste exemplo a consulta retornará todos os documentos da collecion 'products' que `is_available` seja `True` e que tenham `price` maior ou igual a 5

!!! tip
    As entradas para estes Operadores Lógicos podem ser Operadores de Comparação ou mesmo outros Operadores Lógicos. Essa flexibilidade permite criar consultas complexas e aninhadas, permitindo expressar condições complexas de recuperação de dados com precisão.