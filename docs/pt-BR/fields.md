# <center>Fields</center>

No **PyODMongo**, `Fields` é uma extensão do Pydantic Fields, oferecendo o mesmo rico conjunto de funcionalidades enquanto introduz três argumentos adicionais para controle aprimorado sobre a criação de índices em coleções do MongoDB.

```python
from pyodmongo import DbModel, Field
from typing import ClassVar


class User(DbModel):
    name: str = Field(index=True, text_index=True)
    email: str = Field(index=True, unique=True)
    password: str
    is_active: bool
    _collection: ClassVar = 'users'
```

- `index: bool`: Quando definido como `True`, este campo resultará na criação de um índice na coleção usando o mesmo nome do campo.
- `unique: bool`: Quando definido como `True`, este campo faz com que o índice criado seja único. Em outras palavras, dois documentos da coleção não podem ter o mesmo valor para este campo.
- `text_index: bool`: Definir este campo como `True` indica que o campo deve ser incluído nos índices de texto da coleção. Índices de texto são usados para funcionalidade de pesquisa de texto completo.
- `default_language: str`: O idioma padrão que o MongoDb irá setar no índice de texto da collection. Você pode conferir mais detalhes em <a href="https://www.mongodb.com/docs/manual/reference/text-search-languages/#std-label-text-search-languages" target="_blank">Text Search Languages</a>.

Para uma compreensão mais abrangente dos recursos básicos do Field, consulte a <a href="https://docs.pydantic.dev/latest/api/fields/" target="_blank">documentação do Pydantic Fields</a> .