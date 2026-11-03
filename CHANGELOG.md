# Changelog

Todas as mudanças relevantes deste projeto são registradas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e
o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

## [0.3.0] - 2026-11-03

### Adicionado

- Empacotamento Flatpak com runtime Freedesktop 25.08, metadados AppStream,
  ícone, desktop entry e dependências Python fixadas por URL/SHA-256.
- Workflow `Flatpak` para builds em `develop`/`main` e anexo do bundle aos
  releases em tags `v*`.
- Documentação de instalação e build local do Flatpak.
- Workflow de CI também executa em pushes para a branch `develop`.

## [0.2.1] - 2026-11-02

### Corrigido

- Mensagem do `voluta gui` agora diferencia PySide6 ausente de bibliotecas
  de sistema do Qt ausentes (por exemplo, `libGL` no NixOS).

### Adicionado

- `shell.nix` com as bibliotecas necessárias para executar a interface
  gráfica no NixOS.
- Documentação de execução da GUI no NixOS.

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
