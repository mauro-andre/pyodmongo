# <center>Visão geral</center>

![Image title](./assets/images/pyodmongo_Logo_BG_Dark.png#only-dark)
![Image title](./assets/images/pyodmongo_Logo_BG_White.png#only-light)

<div align="center">
    <a href="https://pypi.org/project/pyodmongo/" target="_blank">
      <img src="https://img.shields.io/pypi/v/pyodmongo" alt="coverage">
    </a>
    <a href="https://pypi.org/project/pyodmongo/" target="_blank">
      <img src="https://img.shields.io/badge/Python-3.11-green" alt="pre-commit">
    </a>
</div>

**PyODMongo** é uma biblioteca Python moderna que funciona como um mapeador de objetos-documentos (ODM) robusto para **MongoDB**. Aproveitando o poder do **Pydantic V2**, ele preenche perfeitamente a lacuna entre o Python e o MongoDB, oferecendo uma maneira intuitiva e eficiente de interagir com documentos do MongoDB.

Ao usar o **PyODMongo**, você pode mapear facilmente suas classes Python para documentos MongoDB, permitindo uma abordagem mais Pythonica para lidar com dados. Esta biblioteca simplifica todo o processo de definição e trabalho com coleções, documentos e consultas do MongoDB.

**PyODMongo** é construído sobre **Pydantic V2**, tornando a classe `DbModel` uma extensão da `BaseModel` do Pydantic. Isso significa que toda a rica funcionalidade da `BaseModel` do Pydantic, incluindo **Validators**, **Fields** e **Model Config**, está prontamente disponível em `DbModel`.

## Principais Recursos

- **Integração com pydantic**: Aproveite o poder da validação de dados e das capacidades de modelagem do pydantic ao trabalhar com dados do MongoDB.

- **Geração Automática de Esquema**: Defina o esquema do MongoDB usando modelos pydantic, e o **PyODMongo** criará automaticamente as coleções necessárias no MongoDB, garantindo a consistência dos dados.

- **Construtor de Consultas**: Construa facilmente consultas complexas do MongoDB usando código Python, reduzindo a necessidade de escrever strings de consulta brutas.

- **Serialização de Documentos**: Serialize e desserialize objetos Python para documentos do MongoDB sem esforço.

- **Suporte Assíncrono**: Tire proveito da programação assíncrona com o **PyODMongo** para aprimorar o desempenho de suas operações com o MongoDB.

- **Desenvolvimento Ativo**: O **PyODMongo** está em desenvolvimento ativo e é mantido regularmente, com novos recursos e melhorias sendo adicionados.

## Instalação

Você pode instalar o **PyODMongo** usando pip:

```bash
pip install pyodmongo
```
## Contribuições
Contribuições para o **PyODMongo** são bem-vindas! Se você encontrar problemas ou tiver ideias de melhorias, abra uma issue ou envie uma pull request no [repositório do GitHub](https://github.com/mauro-andre/pyodmongo).

## Licença
**PyODMongo** é licenciado sob a Licença MIT. Consulte o [arquivo LICENSE](https://github.com/mauro-andre/pyodmongo/blob/master/LICENSE) para obter mais informações.