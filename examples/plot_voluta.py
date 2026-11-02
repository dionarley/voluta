"""Gera uma imagem do perfil da voluta usando a API do pacote.

Execute com::

    uv run python examples/plot_voluta.py
"""

from __future__ import annotations

from pathlib import Path

from voluta import plot_volute, volute_profile


def main() -> None:
    profile = volute_profile(r2=100.0, k=25.0, turns=1.5, samples=1000)
    output = Path(__file__).with_name("voluta.png")
    plot_volute(
        profile,
        output=output,
        dpi=150,
        title="Traçado Geométrico da Voluta de um Soprador Centrífugo",
    )
    print(f"Figura gerada em: {output}")


if __name__ == "__main__":
    main()
