# <center>DbModel</center>

No **PyODMongo**, a classe `DbModel` serve como elemento fundamental para modelar coleções MongoDB. Quando você cria uma classe que herda de `DbModel`, ela automaticamente se torna uma representação de uma coleção no MongoDB.

Graças à integração do **PyODMongo** e Pydantic, você pode criar coleções MongoDB e definir seu esquema sem esforço, combinando os pontos fortes do MongoDB com a conveniência das classes Pydantic e suas validações de dados.

```python
__db_model.py__
```

Para garantir que sua classe Python esteja mapeada corretamente para a coleção MongoDB correspondente, é essencial incluir o atributo `_collection`. Este atributo deve ser um `ClassVar` com um valor de string contendo o nome desejado da coleção em seu banco de dados MongoDB.

## Atributos herdados de DbModel

Quando você cria uma classe que herda de `DbModel`, ela não apenas representa uma coleção MongoDB, mas também herda alguns atributos adicionais automaticamente. Esses atributos herdados fornecem metadados essenciais para seus documentos e são criados automaticamente se não forem fornecidos explicitamente ao instanciar objetos.

### `id: Id`

Cada documento derivado de DbModel herda um atributo id, representado pela classe `Id`. Este atributo serve como um identificador exclusivo para o documento dentro de sua coleção MongoDB. Se você não especificar um id ao criar um novo objeto, ele será gerado automaticamente.

!!! note "Id Class"
    Por trás dos panos, o **PyODMongo** processa instâncias da classe `Id` para serem armazenadas como `ObjectId` no MongoDB. Essa transformação é tratada de forma transparente, para que você possa interagir com instâncias `Id` como se fossem strings regulares em seu código Python. Você também tem a flexibilidade de inserir um `str` ou um `ObjectId`, o **PyODMongo** cuidará da conversão.

!!! tip
    O atributo `id` é o mesmo `_id` no MongoDb.

### `created_at: datetime`

O atributo `created_at` no **PyODMongo** é um carimbo de data/hora totalmente gerenciado pela biblioteca **PyODMongo**. Serve como um registro de quando um documento foi criado inicialmente no banco de dados. Este atributo é gerado automaticamente no momento da criação do documento.

### `updated_at: datetime`

Da mesma forma, o atributo `updated_at` no **PyODMongo** é outro carimbo de data/hora totalmente gerenciado pela biblioteca **PyODMongo**. Serve como um indicador de quando um documento foi modificado pela última vez no banco de dados. Este campo é atualizado automaticamente sempre que são feitas alterações no documento.

## Relacionamentos

No **PyODMongo**, você pode modelar relacionamentos entre documentos usando referências e documentos incorporados. Esses relacionamentos permitem representar estruturas e associações de dados complexas em seu banco de dados MongoDB.

### Relacionamento por referência

Os relacionamentos por referência envolvem a referência de um documento a outro usando um identificador. No **PyODMongo**, você pode estabelecer relacionamentos por referência entre documentos incluindo campos que armazenam referências a identificadores de outros documentos.

```python hl_lines="15"
__reference.py__
```

Neste caso, o **PyODMongo** aceitará que `user` pode ser uma instância de `User` ou uma referência `Id`

!!! tip
    Você também pode ter uma lista de referências incluindo `user: list[User | Id]`

### Documentos incorporados

Documentos incorporados envolvem aninhar um documento dentro de outro. No **PyODMongo**, você pode definir relacionamentos incorporados incluindo campos que representam documentos aninhados.

/// tab | PyODMongo MainBaseModel
```python hl_lines="5"
__embedded_mainbasemodel.py__
```
///
/// tab | Pydantic BaseModel
```python hl_lines="6"
__embedded_basemodel.py__
```
///

!!! note
    A diferença entre usar `MainBaseModel` e `BaseModel` é que alguns métodos de busca, como o operador `$elemMatch`, requerem `MainBaseModel` para elementos aninhados. Portanto, é sempre recomendado usar `MainBaseModel`.

!!! tip
    Você também pode incorporar documentos de outros objetos `DbModel` em vez de `BaseModel`. Isso é ótimo quando você deseja manter as informações atuais em um documento.

### Aproveitando Relacionamentos

Ao modelar relacionamentos no **PyODMongo**, você pode criar esquemas de dados mais complexos e estruturados, permitindo construir aplicativos sofisticados que capturam associações de dados do mundo real. Sejam relacionamentos de referência para vincular documentos ou relacionamentos incorporados para aninhar documentos, o **PyODMongo** oferece flexibilidade para projetar seus modelos de dados de acordo com as necessidades da sua aplicação.