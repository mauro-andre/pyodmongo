# <center>Delete</center>

## Delete

O método `delete` está disponível em `AsyncDbEngine` e `DbEngine` e é usado para excluir documentos de uma coleção MongoDB com base em uma consulta especificada. Este método oferece uma maneira direta de remover documentos que atendem à consulta especificada do seu banco de dados MongoDB.

/// tab | Async
```python hl_lines="18"
__delete_async.py__
```
///
/// tab | Sync
```python hl_lines="16"
__delete_sync.py__
```
///

### Argumentos

- `Model: DbModel`: A classe que herda de `DbModel` e serve de base para consulta ao banco de dados.
- `query: ComparisonOperator | LogicalOperator`: Consulta que define os critérios de seleção dos documentos a serem excluídos.
- `raw_query: dict (opcional)`: Uma consulta bruta em formato de dicionário aceita pelo MongoDB.

!!! warning
    Nos bastidores, o método `delete` usa a operação `delete_many` do MongoDB para remover documentos. Todos os documentos que correspondam aos critérios de consulta serão excluídos da coleção.


## Delete one

O método `delete_one` é semelhante ao método `delete`, a principal diferença é que ele excluirá apenas o primeiro documento que corresponder à consulta especificada.

/// tab | Async
```python hl_lines="18-20"
__delete_one_async.py__
```
///
/// tab | Sync
```python hl_lines="16"
__delete_one_sync.py__
```
///

## Resposta do delete
O método `delete` no **PyODMongo** retorna um objeto `DbResponse` que fornece informações sobre o resultado da operação de exclusão. Este objeto contém vários atributos que dão insights sobre como a operação de exclusão afetou o banco de dados.

### Atributos de `DbResponse`

- `acknowledged: bool`: Um valor booleano indicando se a operação foi reconhecida pelo servidor MongoDB. Se a operação foi reconhecida, este atributo é definido como `True`, indicando que o servidor reconheceu e processou a solicitação de salvamento.

- `deleted_count: int`: Um inteiro que representa o número de documentos que foram excluídos do banco de dados como parte da operação de exclusão.

- `inserted_count: int`: Um inteiro que indica o número de documentos que foram inseridos com sucesso no banco de dados durante a operação de inserção.

- `matched_count: int`: Um inteiro que representa o número de documentos no banco de dados que corresponderam à consulta ou critérios especificados durante a operação de salvamento. Este valor indica quantos documentos existentes foram atualizados como parte da operação de salvamento.

- `modified_count: int`: Um inteiro que representa o número de documentos no banco de dados que foram realmente modificados durante a operação de salvamento. Este valor geralmente é igual ou um subconjunto de `matched_count` e indica quantos documentos tiveram seus campos alterados.

- `upserted_count: int`: Um inteiro que representa o número de documentos que foram inseridos como resultado de uma operação upsert. Isso ocorre quando um documento não existe e é criado durante o processo de atualização.

- `upserted_ids: dict[int, Id]`: Um dicionário que mapeia o índice dos documentos inseridos para seus novos IDs únicos. Este atributo é útil para rastrear quais documentos foram criados durante uma operação upsert.