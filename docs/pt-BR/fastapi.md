# <center>Usar com FastAPI</center>

**PyODMongo** é totalmente compatível com FastAPI devido à sua base Pydantic. Essa compatibilidade permite utilizar o **PyODMongo** em aplicações FastAPI de maneira elegante e eficiente, permitindo a criação de consultas dinâmicas em tempo de execução.

```python
__fastapi.py__
```

No exemplo acima, definimos uma rota FastAPI `GET /` que aceita parâmetros de consulta. A função `mount_query_filter`, projetada para uso com `Request` do FastAPI, constrói dinamicamente uma consulta com base nos itens desses parâmetros.

## A Função `mount_query_filter`

A função `mount_query_filter` se adapta perfeitamente com o FastAPI. Ela constrói dinamicamente uma consulta com base nos itens do dicionário passado, tornando-a compatível com o atributo `request.query_params._dict`, que contém as query strings da rota.

### Parâmetros da função

- `Model: DbModel`: A model para a qual a query será construída.
- `items: dict`: O dicionário que contém os items de consulta da query.
- `initial_comparison_operators: list[ComparisonOperator]`: Uma lista inicial de operadores de comparação.

A função retorna uma consulta com o operador `and` aplicado entre todos os itens do dicionário passado.

## Exemplo de uso

![Image title](./assets/images/insomnia_request.png)

Quando você aciona a seguinte rota com query strings: `http://localhost:8000/?attr1_eq=value_1&attr2_in=%5B'value_2',%20'value_3'%5D&attr3_gte=10&_sort=%5B%5B'attr1',%201%5D,%20%5B'attr2',%20-1%5D%5D`, o `request.query_params._dict` irá conter o seguinte dicionário:

```python
{
    "attr1_eq": "value_1", 
    "attr2_in": "['value_2', 'value_3']", 
    "attr3_gte": 10,
    "_sort": "[['attr1', 1], ['attr2', -1]]",
}
```
```

Neste dicionário, as chaves devem ser nomes de atributos seguidos por um sublinhado e um operador válido (por exemplo,  `"attr1" + "_" + "eq"`). Os operadores válidos são: `"eq", "gt", "gte", "in", "lt", "lte", "ne", "nin", "sort"`.

Ao utilizar a função `mount_query_filter` em combinação com `Request` do FastAPI, você pode habilitar recursos de consulta poderosos e dinâmicos em suas aplicações.