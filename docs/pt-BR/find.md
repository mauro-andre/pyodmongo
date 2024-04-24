# <center>Find</center>

## Find one

O método `find_one` está disponível nas classes `AsyncDbEngine` e `DbEngine` da biblioteca **PyODMongo**. Este método é usado para recuperar um único objeto do banco de dados com base em critérios especificados.

/// tab | Async
```python hl_lines="21"
from pyodmongo import AsyncDbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar
import asyncio

# Initialize the database engine
engine = AsyncDbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

# Define a model class
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

async def main():
    # Define a query (in this case, we're using the 'eq' method from 'pyodmongo.queries')
    query = eq(Product.name, 'Box')

    # Use 'find_one' to retrieve a single product based on the query
    result: Product = await engine.find_one(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="19"
from pyodmongo import DbEngine, DbModel
from pyodmongo.queries import eq
from typing import ClassVar

# Initialize the database engine
engine = DbEngine(mongo_uri='mongodb://localhost:27017', db_name='my_db')

# Define a model class
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

# Define a query (in this case, we're using the 'eq' method from 'pyodmongo.queries')
query = eq(Product.name, 'Box')

# Use 'find_one' to retrieve a single product based on the query
result: Product = engine.find_one(Model=Product, query=query)
```
///

### Argumentos

- `Model: type[DbModel]`: A classe que herda de `DbModel` a ser utilizada para formar o objeto recuperado do banco de dados.
- `query: ComparisonOperator | LogicalOperator`: A consulta usada para filtrar os objetos no banco de dados.
- `raw_query: dict`: Uma consulta opcional no formato de dicionário compatível com MongoDB.
- `sort: SortOperator`: Um parâmetro opcional que especifica a ordem de classificação dos resultados. Cada tupla na lista contém um nome de campo e uma direção (`1` para ascendente, `-1` para descendente). Este parâmetro permite organizar os resultados com base em um ou mais campos, ajudando a organizar os dados recuperados conforme requisitos específicos.
- `raw_sort: dict`: Um parâmetro opcional semelhante ao `sort`, mas utiliza um formato de dicionário diretamente compatível com as especificações de classificação do MongoDB. É particularmente útil quando critérios de classificação complexos são necessários e são diretamente suportados pelo MongoDB. Isso pode proporcionar um controle mais direto sobre o processo de classificação na consulta ao banco de dados.
- `populate: bool`: Flag booleana que determina se o objeto retornado terá seus campos de relacionamento preenchidos com outros objetos ou conterá apenas o `id`.
- `as_dict: bool`: Um indicador booleano que, quando definido como `True`, retorna a resposta como um dicionário ao invés de objetos instanciados. Isso é particularmente útil quando um formato leve e serializável é necessário, como para respostas JSON em aplicações web, ou quando o consumidor prefere trabalhar com estruturas de dados básicas ao invés de modelos de objetos complexos.
- `tz_info: timezone`:  Um parâmetro opcional que especifica a informação de fuso horário para quaisquer campos `datetime` nos objetos recuperados. Este parâmetro é crucial ao lidar com registros em diferentes fusos horários e garante que os valores de `datetime` sejam corretamente ajustados para o fuso horário especificado. Se não definido, os campos de `datetime` serão retornados no fuso horário padrão do banco de dados ou do servidor de aplicação.

!!! warning
    Se `raw_query` for passado, `query` não será considerado.

## Find many

O método `find_many` na biblioteca **PyODMongo** é semelhante ao método `find_one`, mas recupera uma lista de objetos que correspondem aos critérios especificados.

/// tab | Async
```python hl_lines="13"
# Define a model class
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

async def main():
    # Define a query (in this case, we're using the 'eq' method from 'pyodmongo.queries')
    query = gte(Product.price, 5)

    # Use 'find_many' to retrieve a list of products based on the query
    result: list[Product] = await engine.find_many(Model=Product, query=query)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="12"
# Define a model class
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

# Define a query (in this case, we're using the 'gte' method from 'pyodmongo.queries')
query = gte(Product.price, 5)

# Use 'find_many' to retrieve a list of products based on the query
result: list[Product] = engine.find_many(Model=Product, query=query)
```
///

### Argumentos

Além disso, inclui três argumentos extras para controle de paginação:

- `paginate: bool`: Flag booleana que especifica se a resposta deve ser paginada ou uma lista regular.
- `current_page: int`: Se `paginate=True`, este argumento determina a página de resultados a ser recuperada.
- `docs_per_page: int`: Se `paginate=True`, este argumento determina o número máximo de objetos por página nos resultados da consulta.

### Paginate

Quando você define `paginate=True` no método `find_many` do **PyODMongo**, o resultado da consulta será encapsulado em um objeto do tipo `ResponsePaginate`. Isso permite a recuperação eficiente e organizada dos resultados da consulta em várias páginas. O objeto `ResponsePaginate` contém os seguintes atributos:

- `current_page: int`: Indica a página atual do resultado da pesquisa.
- `page_quantity: int`: Representa o número total de páginas no resultado da pesquisa.
- `docs_quantity: int`: Especifica a contagem total de objetos encontrados na pesquisa.
- `docs: list[Any]`: Contém a lista de objetos recuperados para a página atual.

Este mecanismo de paginação é particularmente útil ao lidar com grandes conjuntos de dados, pois permite dividir os resultados em partes gerenciáveis e navegar por eles com facilidade.

/// tab | Async
```python hl_lines="9"
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'

async def main():
    query = gte(Product.price, 5)
    result: ResponsePaginate = await engine.find_many(Model=Product, query=query, paginate=True)

asyncio.run(main())
```
///
/// tab | Sync
```python hl_lines="9"
class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = 'products'


query = gte(Product.price, 5)
result: ResponsePaginate = engine.find_many(Model=Product, query=query, paginate=True)
```
///

## Populate

O recurso populate da biblioteca **PyODMongo** é um mecanismo poderoso para preencher automaticamente todas as referências dentro de um objeto, incluindo referências aninhadas. Este recurso simplifica o trabalho com dados relacionados no MongoDB e permite acessar documentos vinculados sem precisar recuperá-los manualmente, um por um. A funcionalidade populate tem o seguinte comportamento:

- Quando você habilita `populate=True` em `find_one` ou `find_many`, o **PyODMongo** preencherá todas as referências dentro desse objeto.
- Se as próprias referências tiverem referências adicionais, o **PyODMongo** também as preencherá recursivamente, percorrendo todos os níveis de referência.
- Listas de referências também são populadas.

!!! note
    Para garantir um excelente desempenho, o **PyODMongo** aproveita o poder da estrutura de agregação do MongoDB. Trata-se de uma ferramenta poderosa e eficiente para processar e transformar dados no MongoDB.

