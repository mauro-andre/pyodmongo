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
    <a href="/coverage" target="_blank">
      <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fs3.amazonaws.com%2Fpyodmongo.dev%2Fcoverage%2Fcoverage_badge.json&logo=pytest" alt="pre-commit">
    </a>
    <a href="https://pepy.tech/project/pyodmongo" target="_blank">
      <img src="https://static.pepy.tech/badge/pyodmongo/month">
    </a>
</div>

**PyODMongo** é uma biblioteca moderna em Python que atua como um robusto Mapeador Objeto-Documento (ODM) e faz uma ponte perfeita entre Python e **MongoDB**. Ela oferece uma maneira intuitiva e eficiente de interagir com documentos.

Construído em cima do **Pydantic V2**, o **PyODMongo** garante que os documentos no banco de dados representem rigorosamente a estrutura dos objetos Python. Isso significa que os documentos são salvos e recuperados do banco de dados exatamente como um objeto Python é estruturado, independentemente de quão aninhados os objetos estejam e se eles estão armazenados de forma persistente ou por referência. O **PyODMongo** pode popular automaticamente esses documentos.

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
Contribuições para o **PyODMongo** são bem-vindas! Se você encontrar problemas ou tiver ideias de melhorias, abra uma issue ou envie uma pull request no <a href="https://github.com/mauro-andre/pyodmongo" target="_blank">repositório do GitHub</a>.

## Licença
**PyODMongo** é licenciado sob a Licença MIT. Consulte o <a href="https://github.com/mauro-andre/pyodmongo/blob/master/LICENSE" target="_blank">arquivo LICENSE</a> para obter mais informações.