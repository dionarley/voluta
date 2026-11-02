# Voluta

**Matemática e geometria de sopradores centrífugos.**

[![CI](https://github.com/dionarley/voluta/actions/workflows/ci.yml/badge.svg)](https://github.com/dionarley/voluta/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-2ea44f.svg)](https://dionarley.github.io/voluta/)
[![Código-fonte](https://img.shields.io/badge/c%C3%B3digo-GitHub-181717?logo=github)](https://github.com/dionarley/voluta)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/gerenciado%20com-uv-261230.svg)](https://docs.astral.sh/uv/)
[![Licença: MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green.svg)](LICENSE)
[![Testes](https://img.shields.io/badge/testes-pytest-0a9edc.svg)](tests/)

![Voluta Project — A Python-powered Centrifugal Blower Design & Flow Generator](docs/assets/voluta-project-hero.jpeg)

Projeto de referência para a geometria e o dimensionamento preliminar de
**sopradores centrífugos**. Reúne as equações de turbomáquinas do documento
[Matemática dos Sopradores](docs/assets/matematica-dos-sopradores.pdf) em uma
biblioteca Python testável, uma CLI e documentação com as fórmulas.

O nome **Voluta** vem da carcaça em espiral do soprador, responsável por
converter a energia cinética do ar em pressão estática.

## O que o projeto faz

- Traça a **voluta em espiral de Arquimedes**: `R(θ) = R₂ + K · θ / 2π`.
- Calcula **triângulo de velocidades**, equação de Euler e velocidade periférica.
- Dimensiona **diâmetros de entrada e saída**, largura de pá e potência no eixo.
- Aplica as **leis de afinidade** para mudança de rotação e diâmetro.
- Gera **imagens** do perfil da voluta em PNG, SVG ou PDF.
- Oferece uma **CLI** (`voluta plot`, `voluta design` e `voluta gui`) e uma API Python.
- Inclui uma **interface gráfica Qt** com pré-visualização do perfil e
  calculadora de dimensionamento.

### Perfil gerado pelo projeto

![Geometria da voluta e do rotor](docs/assets/voluta.svg)

> O dimensionamento implementado é preliminar. Perdas, curvas reais do rotor,
> seleção de motor, resistência mecânica e ruído devem ser verificados em um
> projeto de engenharia completo.

## Requisitos

- Python 3.10 ou superior
- [uv](https://docs.astral.sh/uv/) para instalação e execução

Instale o `uv`, caso ainda não tenha:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Instalação

```bash
git clone https://github.com/dionarley/voluta.git
cd voluta
uv sync
```

O comando cria o ambiente virtual em `.venv/`, instala o pacote em modo
editável e baixa as dependências de desenvolvimento e documentação.

## Binários pré-compilados

A cada tag `v*`, o workflow **Binaries** gera executáveis standalone com
PyInstaller e publica no [GitHub Releases](https://github.com/dionarley/voluta/releases/latest).

| Plataforma | Arquivo |
| --- | --- |
| Linux x86_64 | `voluta-linux-x86_64` |
| macOS Intel | `voluta-macos-x86_64` |
| macOS Apple Silicon | `voluta-macos-arm64` |
| Windows x86_64 | `voluta-windows-x86_64.exe` |

Linux e macOS:

```bash
chmod +x voluta-linux-x86_64
./voluta-linux-x86_64 --version
```

No macOS, se o sistema bloquear o executável por quarentena:

```bash
xattr -d com.apple.quarantine voluta-macos-arm64
```

Windows:

```powershell
.\voluta-windows-x86_64.exe --version
```

Os binários não são assinados digitalmente. O Windows pode exibir o aviso do
SmartScreen e o macOS pode pedir confirmação no primeiro uso.

## Início rápido

Gerar a imagem padrão da voluta:

```bash
uv run voluta plot --output voluta.png
```

Dimensionar um soprador com vazão de `0,5 m³/s`, elevação de pressão de
`1.200 Pa` e rotação de `3.000 RPM`:

```bash
uv run voluta design --flow 0.5 --pressure 1200 --rpm 3000
```

Saída em JSON, útil para scripts:

```bash
uv run voluta design --flow 0.5 --pressure 1200 --rpm 3000 --json
```

Também é possível executar como módulo:

```bash
uv run python -m voluta --help
```

## Interface gráfica (Qt)

A interface usa **PySide6** (Qt para Python) e matplotlib. Ela permite ajustar
os parâmetros da voluta, visualizar o perfil em tempo real, calcular o
dimensionamento e exportar a imagem ou o resultado em JSON.

```bash
uv sync --group gui
uv run voluta gui
```

Também é possível instalar a interface como extra do pacote:

```bash
pip install ".[gui]"
voluta gui
```

![Interface gráfica do Voluta](docs/assets/voluta-gui.png)

## Uso como biblioteca

```python
from voluta import design_blower, plot_volute, volute_profile

# Perfil geométrico da voluta
perfil = volute_profile(r2=100.0, k=25.0, turns=1.5)
print(perfil.outlet_radius)  # 137.5

# Imagem do perfil
plot_volute(perfil, output="voluta.png", dpi=150)

# Dimensionamento preliminar (SI: m³/s, Pa, RPM)
projeto = design_blower(
    flow_rate_m3_s=0.5,
    pressure_rise_pa=1200.0,
    rpm=3000.0,
    pressure_coefficient=0.6,
    inlet_velocity_m_s=20.0,
    efficiency=0.7,
)
print(f"D2 = {projeto.outlet_diameter_mm:.1f} mm")
print(f"Potência = {projeto.shaft_power_kw:.2f} kW")
```

Consulte [docs/uso.md](docs/uso.md) para todos os comandos e exemplos.

## Equações implementadas

| Grandeza | Equação | Função |
| --- | --- | --- |
| Velocidade periférica | `U = π D N / 60` | `peripheral_velocity` |
| Pressão teórica (Euler) | `ΔP_th = ρ (U₂ C_u2 − U₁ C_u1)` | `euler_pressure` |
| Diâmetro de saída | `U₂ = √(2 ΔP / (ρ ψ))`, `D₂ = 60 U₂ / (π N)` | `outlet_diameter` |
| Diâmetro de entrada | `D₁ = √(4 Q / (π C_1m))` | `inlet_diameter` |
| Largura da pá | `b = Q / (π D C_m)` | `blade_width` |
| Potência no eixo | `P = Q ΔP / η` | `shaft_power` |
| Voluta | `R(θ) = R₂ + K θ / 2π` | `volute_radius` |
| Leis de afinidade | `Q ∝ N D³`, `ΔP ∝ N² D²`, `P ∝ N³ D⁵` | `affinity_*` |

A dedução e as hipóteses estão em [docs/matematica.md](docs/matematica.md).

## Estrutura do projeto

```text
.
├── .github/workflows/          # CI, Pages e binários
│   ├── binaries.yml
│   ├── ci.yml
│   └── docs.yml
├── docs/                       # documentação MkDocs
│   ├── assets/                 # banner, screenshot, PDF e SVG
│   ├── api.md
│   ├── index.md
│   ├── matematica.md
│   ├── referencias.md
│   └── uso.md
├── examples/                   # scripts de exemplo
├── scripts/entrypoint.py       # entrada do PyInstaller
├── src/voluta/                 # código-fonte do pacote
│   ├── aero.py                 # equações de dimensionamento
│   ├── cli.py                  # interface de linha de comando
│   ├── geometry.py             # voluta e perfil cartesiano
│   ├── gui.py                  # interface gráfica Qt
│   └── plots.py                # visualização com matplotlib
├── tests/                      # testes com pytest
├── LICENSE                     # licença MIT
├── pyproject.toml              # metadados, dependências e ferramentas
├── README.md
└── uv.lock                     # resolução reproduzível do uv
```

## Desenvolvimento

```bash
uv sync                     # instala dependências
uv run pytest               # executa os testes
uv run pytest --cov         # testes com cobertura
uv run ruff check .         # análise estática
uv run ruff format --check .  # verifica formatação
```

Gerar a documentação localmente:

```bash
uv run mkdocs serve
```

Acesse <http://127.0.0.1:8000>. Para validar o build:

```bash
uv run mkdocs build --strict
```

## Documentação

Documentação publicada: **https://dionarley.github.io/voluta/**

- [Visão geral](docs/index.md)
- [Matemática](docs/matematica.md)
- [Uso e API](docs/uso.md)
- [Referência da API](docs/api.md)
- [Referências](docs/referencias.md)

## Licença

Distribuído sob a licença **MIT**. Consulte [LICENSE](LICENSE).
