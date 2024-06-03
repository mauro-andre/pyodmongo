# <center>Aggregation</center>

Aggregation é um recurso fantástico do MongoDB que permite realizar várias transformações e análises de dados. Embora o Aggregation Pipeline do MongoDB seja uma ferramenta poderosa, às vezes pode ser complexo trabalhar com ele devido aos seus estágios e expressões, porém uma vez dominando a ferramenta, ela se torna um poderoso aliado na análise de dados.

No **PyODMongo**, oferecemos a você a capacidade de aproveitar todo o poder da estrutura de agregação do MongoDB e para usa-lo você precisa estar familiarizado com esse recurso.

Para utilizar os recursos de agregação no **PyODMongo**, você pode inserir pipelines de agregação diretamente em seus modelos. Tudo que você precisa fazer é criar um atributo de classe chamado `_pipeline` em seu modelo e definir os estágios de agregação. Quando você usa os métodos `find_one` ou `find_many` do **PyODMongo**, a biblioteca executará o pipeline de agregação e retornará o resultado como objetos Python.

Aqui está um exemplo simples usando apenas o estágio `$group` do MongoDB Aggregation Pipeline:

/// tab | Async
```python
__aggregation_async.py__
```
///
/// tab | Sync
```python
__aggregation_sync.py__
```
///

!!! tip
    PyODMongo já utiliza agregação nos métodos `find` e `find_one` internamente. O parâmetro `query` nesses métodos é na verdade convertido em uma etapa `$match` e inserido como a primeira etapa do pipeline de agregação. Você pode continuar usando essa combinação passando o parâmetro `query` nos métodos `find` e `find_one` e `_pipeline` na sua classe.

Neste exemplo, temos um modelo `OrdersByCustomers` com um pipeline de agregação que agrupa os pedidos por cliente, calculando a contagem de pedidos e o valor total para cada cliente.

**PyODMongo** oferece flexibilidade no uso da agregação, mas é essencial garantir que a saída esteja alinhada com os campos definidos na sua classe para evitar erros ao instanciar objetos.

Com o suporte de agregação do PyODMongo, você pode desbloquear todo o potencial dos recursos de transformação de dados do MongoDB, mantendo uma experiência de codificação Pythônica e intuitiva. As possibilidades de análise e processamento de dados são praticamente ilimitadas.