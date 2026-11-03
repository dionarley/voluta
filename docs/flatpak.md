# Flatpak

O Voluta pode ser distribuído como **Flatpak** para Linux, sem depender da
distribuição ou das bibliotecas Qt instaladas no sistema.

## Instalar o bundle

O bundle é publicado no [GitHub Releases](https://github.com/dionarley/voluta/releases/latest)
a cada tag `v*`. Baixe `voluta.flatpak` e instale:

```bash
flatpak install --user voluta.flatpak
flatpak run io.github.dionarley.voluta
```

Também é possível iniciar a interface gráfica pelo menu de aplicativos do
ambiente desktop.

## Construir localmente

Pré-requisitos:

- `flatpak`
- `flatpak-builder`
- `appstream`
- `desktop-file-utils`
- acesso ao repositório Flathub

Adicione o Flathub e instale o runtime/SDK usados pelo manifesto:

```bash
flatpak remote-add --user --if-not-exists \
  flathub https://flathub.org/repo/flathub.flatpakrepo

flatpak install --user -y flathub \
  org.freedesktop.Platform//25.08 \
  org.freedesktop.Sdk//25.08
```

Compile e gere o bundle:

```bash
flatpak-builder \
  --user \
  --assumeyes \
  --force-clean \
  --default-branch=stable \
  --repo=repo \
  build-dir \
  flatpak/io.github.dionarley.voluta.yml

flatpak build-bundle repo voluta.flatpak io.github.dionarley.voluta stable
```

Instale e execute:

```bash
flatpak install --user -y --bundle voluta.flatpak
flatpak run io.github.dionarley.voluta
```

## Testes do empacotamento

```bash
flatpak run io.github.dionarley.voluta --version
flatpak run --env=QT_QPA_PLATFORM=offscreen \
  io.github.dionarley.voluta gui --smoke-test
```

O workflow **Flatpak** executa esses testes a cada push ou pull request que
altere o manifesto, o código-fonte ou o `pyproject.toml` nas branches
`develop` e `main`. Em tags `v*`, o bundle também é anexado ao GitHub Releases.

## Estrutura do empacotamento

| Arquivo | Função |
| --- | --- |
| `flatpak/io.github.dionarley.voluta.yml` | manifesto do Flatpak |
| `flatpak/python3-requirements.json` | wheels Python fixadas com URL e SHA-256 |
| `flatpak/io.github.dionarley.voluta.desktop` | entrada do menu de aplicativos |
| `flatpak/io.github.dionarley.voluta.metainfo.xml` | metadados AppStream |
| `flatpak/io.github.dionarley.voluta.svg` | ícone escalável |
| `flatpak/voluta.sh` | wrapper que executa `python3 -m voluta` |

O manifesto usa o runtime `org.freedesktop.Platform` 25.08 e instala as
dependências Python a partir de wheels manylinux. O PySide6 já inclui as
bibliotecas Qt necessárias; o runtime fornece as bibliotecas de sistema
básicas, como `libGL`, `libxkbcommon`, `xcb` e `libX11`.
