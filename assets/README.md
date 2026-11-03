# Assets

Arquivos estáticos compartilhados entre o README, a documentação publicada e o
empacotamento Flatpak.

| Arquivo | Uso |
| --- | --- |
| `voluta-icon.svg` | ícone do aplicativo, logo/favicon do site e README |
| `voluta-project-hero.jpeg` | banner do README e da página inicial |
| `voluta-gui.png` | captura da interface gráfica |
| `voluta.svg` | perfil da voluta gerado pelo projeto |
| `matematica-dos-sopradores.pdf` | documento de referência |

O build do MkDocs sincroniza este diretório com `docs/assets` por meio do hook
`hooks/copy_assets.py`; em seguida, o MkDocs publica os arquivos em
`site/assets`. Assim, existe uma única fonte para os arquivos estáticos.
