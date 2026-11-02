# Changelog

Todas as mudanças relevantes deste projeto são registradas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e
o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

## [0.2.0] - 2026-11-02

### Adicionado

- Interface gráfica Qt com PySide6 para geometria e dimensionamento.
- Pré-visualização do perfil da voluta em tempo real.
- Exportação de imagem e de dimensionamento em JSON pela interface.
- Comando `voluta gui` e extra opcional `voluta[gui]`.
- Testes da interface gráfica em modo headless.
- Smoke test da GUI nos binários de Linux, macOS e Windows.

## [0.1.0] - 2026-11-02

### Adicionado

- Pacote `voluta` com geometria da voluta, equações de dimensionamento e
  visualização.
- CLI `voluta plot` e `voluta design`.
- Leis de afinidade para rotação e diâmetro.
- Testes com `pytest` para geometria, aerodinâmica, gráficos e CLI.
- Binários standalone para Linux, macOS e Windows via GitHub Actions e
  PyInstaller.
- Documentação com MkDocs Material, incluindo a matemática e a referência da
  API.
- Licença MIT.
- Integração contínua com GitHub Actions.
- Preservação do PDF, do SVG e do script originais.
