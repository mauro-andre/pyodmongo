# <center>Índices</center>

Os índices desempenham um papel crucial na otimização do desempenho do banco de dados, e o **PyODMongo** oferece opções flexíveis para defini-los e gerenciá-los. Esta seção irá guiá-lo sobre como criar índices usando PyODMongo.

## Criação simples de índice

A maneira mais simples de criar índices no **PyODMongo** é usando o `Field`, especificando qual campo deve ser indexado.

```python
from pyodmongo import DbModel, Field
from typing import ClassVar


class Product(DbModel):
    name: str = Field(index=True)
    code: str = Field(index=True, unique=True)
    description: str = Field(text_index=True, default_language='english')
    price: float
    product_type: str
    is_available: bool
    _collection: ClassVar = 'products'
```

- `index: bool`: Quando definido como `True`, este campo resultará na criação de um índice na coleção usando o mesmo nome do campo.
- `unique: bool`: Quando definido como `True`, este campo faz com que o índice criado seja único. Em outras palavras, dois documentos da coleção não podem ter o mesmo valor para este campo.
- `text_index: bool`: Definir este campo como `True` indica que o campo deve ser incluído nos índices de texto da coleção. Índices de texto são usados para funcionalidade de pesquisa de texto completo.
- `default_language: str`: O idioma padrão que o MongoDb irá setar no índice de texto da collection. Você pode conferir mais detalhes em <a href="https://www.mongodb.com/docs/manual/reference/text-search-languages/#std-label-text-search-languages" target="_blank">Text Search Languages</a>.

## Criação avançada de índice

No entanto, se precisar criar índices mais específicos ou complexos, você pode utilizar o `IndexModel` do PyMongo. Para fazer isso, defina um atributo de nível de classe `_indexes` como uma lista de instâncias de `IndexModel`. Você pode encontrar informações detalhadas sobre a criação de índices com PyMongo em sua <a href="https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_indexes" target=" _blank">documentação oficial</a>.

Aqui está um exemplo de como criar índices personalizados no PyODMongo:

```python
from pyodmongo import DbModel
from pymongo import IndexModel, ASCENDING, DESCENDING
from typing import ClassVar


class Product(DbModel):
    name: str
    code: str
    description: str
    price: float
    product_type: str
    is_available: bool
    _collection: ClassVar = 'products'
    _indexes: ClassVar = [
        IndexModel([('name', ASCENDING), ('price', DESCENDING)], name='name_and_price'),
        IndexModel([('product_type', DESCENDING)], name='product_type'),
    ]
```

Neste exemplo, definimos dois índices personalizados para o modelo `Product` usando `IndexModel`. O primeiro índice é um índice composto do campo `name` em ordem crescente e do campo `price` em ordem decrescente, denominado 'name_and_price'. O segundo índice está no campo `product_type` em ordem decrescente, denominado 'product_type'.

PyODMongo oferece suporte à criação de qualquer estrutura de índice seguindo as diretrizes de estrutura de índice do PyMongo. Essa flexibilidade permite otimizar o desempenho do seu banco de dados de acordo com seus requisitos específicos.