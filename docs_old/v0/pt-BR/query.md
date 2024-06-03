# <center>Query</center>

Criar consultas no **PyODMongo** é simples e intuitivo. Ele simplifica o processo de criação de consultas do MongoDB, fornecendo uma abordagem Pythônica e direta para trabalhar com **Operadores de comparação** e **Operadores lógicos** encontrados no MongoDB.

No **PyODMongo**, uma consulta serve como um atributo essencial dos métodos `find_many` e `find_one`, que estão disponíveis através das classes `DbEngine` e `AsyncDbEngine`. Esses métodos permitem recuperar dados do seu banco de dados MongoDB com facilidade, combinando a simplicidade do Python com os recursos robustos de consulta do MongoDB.

## Operadores de comparação

| Operador | Uso |
| ---------|--- |
| **EQ**  | `eq(Model.attr, value)`</br>`Model.attr == value` |
| **GT**   | `gt(Model.attr, value)`</br>`Model.attr > value` |
| **GTE** | `gte(Model.attr, value)`</br>`Model.attr >= value` |
| **IN**        | `in_(Model.attr, value)` |
| **LT**   | `lt(Model.attr, value)`</br>`Model.attr < value` |
| **LTE** | `lte(Model.attr, value)`</br>`Model.attr <= value` |
| **NE**  | `ne(Model.attr, value)`</br>`Model.attr != value` |
| **NIN**            | `nin(Model.attr, value)` |


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
    query =  Product.price >= 5
    #query = gte(Product.price, 5)
    sort_oprator = sort((Product.name, 1), (Product.price, -1))
    result: Product = await engine.find_one(Model=Product, query=query, sort=sort_oprator)

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


query =  Product.price >= 5
#query = gte(Product.price, 5)
sort_oprator = sort((Product.name, 1), (Product.price, -1))
result: Product = engine.find_one(Model=Product, query=query, sort=sort_oprator)
```
///

Neste exemplo, a consulta retornará todos os documentos da collection 'products' onde o campo price for igual ou superior a 5.

## Operadores lógicos

Assim como os operadores de comparação, os operadores lógicos no **PyODMongo** são projetados para espelhar seus equivalentes no próprio MongoDB.

Aqui estão os principais operadores lógicos disponíveis no PyODMongo:

| Operador | Uso |
| ---------|-|
| **AND**| `and_(gt(Model.attr_1, value_1), lt(Model.attr_1, value_2))`</br>`(Model.attr_1 > value_1) & (Model.attr_1 < value_2)` |
| **OR** | `or_(eq(Model.attr_1, value_1), eq(Model.attr_1, value_2))`</br>`(Model.attr_1 == value_1) | (Model.attr_1 == value_2)` |
| **NOR** | `nor(Model.attr_1 == value_1, Model.attr_1 == value_2)` |


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
    query = (Product.is_available == True) & (Product.price >= 5)
    # query = and_(
    #     eq(Product.is_available, True),
    #     gte(Product.price, 5)
    # )
    sort_oprator = sort((Product.name, 1), (Product.price, -1))
    result: Product = await engine.find_one(Model=Product, query=query, sort=sort_oprator)

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


query = (Product.is_available == True) & (Product.price >= 5)
# query = and_(
#     eq(Product.is_available, True),
#     gte(Product.price, 5)
# )
sort_oprator = sort((Product.name, 1), (Product.price, -1))
result: Product = engine.find_one(Model=Product, query=query, sort=sort_oprator)

```
///

Neste exemplo a consulta retornará todos os documentos da collecion 'products' que `is_available` seja `True` e que tenham `price` maior ou igual a 5

!!! tip
    As entradas para estes Operadores Lógicos podem ser Operadores de Comparação ou mesmo outros Operadores Lógicos. Essa flexibilidade permite criar consultas complexas e aninhadas, permitindo expressar condições complexas de recuperação de dados com precisão.

    ## Sort

/// tab | Async
```python hl_lines="19"
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
    query = Product.price >= 5
    sort_oprator = sort((Product.name, 1), (Product.price, -1))
    result: Product = await engine.find_one(Model=Product, query=query, sort=sort_oprator)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="17"
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


query = Product.price >= 5
sort_oprator = sort((Product.name, 1), (Product.price, -1))
result: Product = engine.find_one(Model=Product, query=query, sort=sort_oprator)
```
///

No exemplo fornecido, o `sort_operator` é definido usando a função `sort`, que aceita tuplas. Cada tupla contém dois elementos: o primeiro é o campo pelo qual você deseja ordenar e o segundo é a direção da ordenação, onde 1 indica ordem ascendente e -1 indica ordem descendente. No caso apresentado, o `sort_operator` ordena os resultados primeiro pelo campo name em ordem ascendente e, em seguida, pelo campo price em ordem descendente. Assim, os produtos são retornados em ordem alfabética pelo nome e, em caso de empate, em ordem decrescente pelo preço.