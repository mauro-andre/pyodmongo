# <center>Operadores de queries</center>

Criar consultas no **PyODMongo** é simples e intuitivo. Ele simplifica o processo de construção de consultas no MongoDB, fornecendo uma abordagem pythônica e direta.

No **PyODMongo**, uma consulta serve como um atributo essencial dos métodos `find_many`, `find_one`, `delete` e `save`, que estão disponíveis através das classes `DbEngine` e `AsyncDbEngine`. Esses métodos permitem que você recupere dados do seu banco de dados MongoDB com facilidade, combinando a simplicidade do Python com as robustas capacidades de consulta do MongoDB.

## Operadores

### Equal (Igual)
O operador **Equal** é usado para combinar documentos onde o valor de um campo é igual ao valor especificado. É um operador básico de comparação no MongoDB e **PyODMongo**.

/// tab | Magic method
```python hl_lines="14"
__eq_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__eq_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{name: {$eq: "Box"}}
```

### Greater than (Maior que)
O operador **Greater than** é usado para combinar documentos onde o valor de um campo é maior que o valor especificado. Ele ajuda a filtrar registros que excedem um determinado limite.

/// tab | Magic method
```python hl_lines="14"
__gt_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__gt_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{price: {$gt: 10}}
```

### Greater than equal (Maior ou igual que)
O operador **Greater than equal** combina documentos onde o valor de um campo é maior ou igual ao valor especificado. Isso é útil para consultas de intervalo que incluem o valor limite.

/// tab | Magic method
```python hl_lines="14"
__gte_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__gte_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{price: {$gte: 10}}
```

### In (Em)
O operador **In** permite especificar um array de valores possíveis para um campo. Ele combina documentos onde o valor do campo está no array especificado.

/// tab | PyODMongo queries
```python hl_lines="3 15"
__in_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{name: {$in: ["Ball", "Box", "Toy"]}}
```

### Lower than (Menor que)
O operador **Lower than** combina documentos onde o valor de um campo é menor que o valor especificado. Isso é usado para filtrar registros abaixo de um determinado limite.

/// tab | Magic method
```python hl_lines="14"
__lt_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__lt_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{price: {$lt: 10}}
```

### Lower than equal (Menor ou igual que)
O operador **Lower than equal** combina documentos onde o valor de um campo é menor ou igual ao valor especificado. Isso inclui o valor limite nos resultados.

/// tab | Magic method
```python hl_lines="14"
__lte_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__lte_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{price: {$lte: 10}}
```

### Not equal (Diferente)
O operador **Not equal** combina documentos onde o valor de um campo não é igual ao valor especificado. Ele é usado para excluir documentos com um valor específico.

/// tab | Magic method
```python hl_lines="14"
__ne_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__ne_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{name: {$ne: "Box"}}
```

### Not in (Não em)
O operador **Not in** permite especificar um array de valores aos quais o campo não deve ser igual. Ele combina documentos onde o valor do campo não está no array especificado.

/// tab | PyODMongo queries
```python hl_lines="3 15"
__nin_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{name: {$nin: ["Ball", "Box", "Toy"]}}
```

### And (E)
O operador **And** é usado para unir várias cláusulas de consulta com um **E** lógico. Ele garante que todas as condições especificadas sejam verdadeiras para que um documento seja incluído no conjunto de resultados.

/// tab | Magic method
```python hl_lines="14"
__and_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__and_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{$and: [{price: {$gt: 10}}, {price: {$lte: 50}}]}
```

### Or (Ou)
O operador **Or** une cláusulas de consulta com um **OU** lógico, combinando documentos que satisfazem pelo menos uma das condições especificadas.

/// tab | Magic method
```python hl_lines="14"
__or_magic.py__
```
///

/// tab | PyODMongo queries
```python hl_lines="3 15"
__or_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{$or: [{name: {$eq: "Box"}}, {price: {$eq: 100}}]}
```

### Nor
O operador **Nor** une cláusulas de consulta com um **NOR** lógico, combinando documentos que não atendem a nenhuma das condições especificadas.

/// tab | PyODMongo queries
```python hl_lines="3 15"
__nor_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{$nor: [{name: {$eq: "Box"}}, {price: {$eq: 100}}]}
```

### Elem match
O operador **Elem match** é usado para combinar documentos que contêm um campo de array com pelo menos um elemento que corresponde a todos os critérios especificados.

/// tab | PyODMongo queries
```python hl_lines="3 20"
__elem_match_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{$products: {$elemMatch: {name: "Box", price: 50}}}
```

### Sort
O operador **Sort** organiza os resultados de uma consulta em uma ordem especificada. Ele é útil para organizar os dados em ordem ascendente ou descendente com base em um campo particular.

/// tab | PyODMongo queries
```python hl_lines="3 16"
__sort_pyodmongo_queries.py__
```
///

Filtro equivalente no MongoDB
```javascript
{name: 1, price: -1}
```