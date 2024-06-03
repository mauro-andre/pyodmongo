# <center>Primeiros passos</center>

Neste guia, orientaremos você nas etapas iniciais para começar a usar o **PyODMongo**, um Mapeador de Objetos-Documentos (ODM) do MongoDB em Python. Abordaremos a criação de um motor, a definição de um modelo, o salvamento de dados e a leitura do banco de dados.

## Criando o motor

Para começar a usar o **PyODMongo**, primeiro você precisa criar uma instância da classe `AsyncDbEngine` ou `DbEngine` para se conectar ao seu servidor MongoDB. Veja como você pode fazer isso:

/// tab | Async
```python hl_lines="5"
__save_async.py__
```
///

/// tab | Sync
```python hl_lines="4"
__save_sync.py__
```
///

Certifique-se de substituir `mongodb://localhost:27017` pela string de conexão com seu banco de dados do MongoDB e `my_db` pelo nome do banco.

!!! tip
    Ao criar um motor, você pode passar o parâmetro `tz_info` nas classes `AsyncDbEngine` ou `DbEngine` que define o fuso horário padrão para todas as operações de `find_one` e `find_many` realizadas através deste motor, a menos que `tz_info` também seja passado nos métodos `find_one` e `find_many`. Neste caso o fuso horário dos métodos de busca terão prevalência.

## Definindo um modelo
A seguir, você definirá um modelo que herda de DbModel. Este modelo representa a estrutura dos seus documentos MongoDB. Você também precisará criar o atributo `_collection`, que carregará a string do nome da coleção a ser salva no banco de dados.

/// tab | Async
```python hl_lines="8 12"
__save_async.py__
```
///

/// tab | Sync
```python hl_lines="7 11"
__save_sync.py__
```
///

Neste exemplo, criamos uma classe `Product`, que herda de `DbModel`, para definir a estrutura de nossos documentos no MongoDB.

## Salvando dados
Você pode salvar dados no MongoDB usando o método `save()` da sua instância `AsyncDbEngine` ou `DbEngine`.

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

Este código cria um novo documento usando os dados fornecidos e salva no MongoDB.

## Lendo do banco de dados
Para ler dados do banco de dados, você pode usar o método `find_one()` da sua instância `AsyncDbEngine` ou `DbEngine`.

/// tab | Async
```python hl_lines="17"
__find_one_async.py__
```
///

/// tab | Sync
```python hl_lines="15"
__find_one_sync.py__
```
///

Este código consulta o banco de dados em busca de um produto com o nome 'Box' e cria um objeto do tipo `Product` com o documento encontrado no banco de dados.

Estes são os primeiros passos para você começar a usar o **PyODMongo**. Agora você pode criar, salvar e ler dados de seu banco de dados MongoDB usando este Mapeador de Objetos-Documentos MongoDB em Python.