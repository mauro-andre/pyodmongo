# <center>Save</center>

## Save

O método `save` faz parte das classes `AsyncDbEngine` e `DbEngine` no **PyODMongo**. É responsável por salvar ou atualizar documentos no banco de dados.

/// tab | Async
```python hl_lines="19"
__save_async.py__
```
///

/// tab | Sync
```python hl_lines="16"
__save_sync.py__
```
///

Se o resultado do método `save` corresponder à criação de um novo documento no banco de dados, a instância do objeto receberá os atributos `id`, `created_at` e `updated_at`.

## Argumentos

- `obj: Any`: Objeto a ser salvo no banco de dados.
- `query: ComparisonOperator | LogicalOperator = None`: Consulta usada para atualizar documentos correspondentes. Caso não seja fornecido, o documento no banco de dados com `_id` igual a `obj.id` será atualizado. Se `obj` não tiver um `id`, um novo documento será criado no banco de dados.
- `raw_query: dict = None`: Consulta no formato aceito pelo MongoDB. Este parâmetro permite especificar uma consulta personalizada para atualização de documentos.

!!! warning
    Se `query` for passado, `raw_query` não será considerado.

!!! note
    Por trás dos panos, o **PyODMongo** usa a operação `update_many` com `upsert=True`, o que significa que ele pode adicionar ou atualizar um ou vários documentos.


## Save all

Além do método `save`, **PyODMongo** fornece o método `save_all`, que permite salvar uma lista de objetos. Este método é particularmente útil quando você precisa salvar vários documentos.

/// tab | Async
```python hl_lines="30"
__save_all_async.py__
```
///
/// tab | Sync
```python hl_lines="28"
__save_all_sync.py__
```
///

## Resposta do save

O método `save` no **PyODMongo** retorna um objeto `DbResponse` que fornece informações sobre o resultado da operação de salvamento. Este objeto contém vários atributos que dão informações sobre como a operação de salvamento afetou o banco de dados.

O valor de retorno de um método `save_all` é um dicionário onde as chaves são os nomes das coleções e os valores são objetos `DbResponse`.

### Atributos de `DbResponse`

- `acknowledged: bool`: Um valor booleano indicando se a operação foi reconhecida pelo servidor MongoDB. Se a operação foi reconhecida, este atributo é definido como `True`, indicando que o servidor reconheceu e processou a solicitação de salvamento.

- `deleted_count: int`: Um inteiro que representa o número de documentos que foram excluídos do banco de dados como parte da operação de exclusão.

- `inserted_count: int`: Um inteiro que indica o número de documentos que foram inseridos com sucesso no banco de dados durante a operação de inserção.

- `matched_count: int`: Um inteiro que representa o número de documentos no banco de dados que corresponderam à consulta ou critérios especificados durante a operação de salvamento. Este valor indica quantos documentos existentes foram atualizados como parte da operação de salvamento.

- `modified_count: int`: Um inteiro que representa o número de documentos no banco de dados que foram realmente modificados durante a operação de salvamento. Este valor geralmente é igual ou um subconjunto de `matched_count` e indica quantos documentos tiveram seus campos alterados.

- `upserted_count: int`: Um inteiro que representa o número de documentos que foram inseridos como resultado de uma operação upsert. Isso ocorre quando um documento não existe e é criado durante o processo de atualização.

- `upserted_ids: dict[int, Id]`: Um dicionário que mapeia o índice dos documentos inseridos para seus novos IDs únicos. Este atributo é útil para rastrear quais documentos foram criados durante uma operação upsert.