"""Visualização do perfil da voluta com matplotlib."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle

from .geometry import VoluteProfile, volute_profile

DEFAULT_TITLE = "Traçado Geométrico da Voluta de um Soprador Centrífugo"


def draw_volute(
    ax: Axes,
    profile: VoluteProfile,
    *,
    title: str = DEFAULT_TITLE,
) -> Axes:
    """Desenha o perfil da voluta e o rotor em um eixo matplotlib existente.

    Parameters
    ----------
    ax:
        Eixo matplotlib onde o desenho será feito. O eixo é limpo antes.
    profile:
        Perfil geométrico calculado por :func:`voluta_profile`.
    title:
        Título do gráfico.

    Returns
    -------
    matplotlib.axes.Axes
        O próprio eixo, para encadeamento.
    """
    ax.clear()
    ax.plot(
        profile.x,
        profile.y,
        label="Perfil da Voluta (Espiral)",
        color="#1f77b4",
        linewidth=2.5,
    )

    impeller = Circle(
        (0, 0),
        profile.r2,
        color="#ff7f0e",
        alpha=0.4,
        label="Rotor ($D_2$)",
    )
    ax.add_patch(impeller)

    ax.axhline(0, color="grey", linewidth=0.8, linestyle="--")
    ax.axvline(0, color="grey", linewidth=0.8, linestyle="--")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("Eixo X (mm)", fontsize=10)
    ax.set_ylabel("Eixo Y (mm)", fontsize=10)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.axis("equal")
    ax.legend(loc="upper right")
    return ax


def plot_volute(
    profile: VoluteProfile | None = None,
    *,
    r2: float = 100.0,
    k: float = 25.0,
    turns: float = 1.5,
    samples: int = 1000,
    output: str | Path | None = None,
    dpi: int = 150,
    show: bool = False,
    title: str = DEFAULT_TITLE,
) -> Figure:
    """Plota o perfil da voluta e o rotor.

    Se ``profile`` não for informado, o perfil é criado com ``volute_profile``
    usando ``r2``, ``k``, ``turns`` e ``samples``.

    Parameters
    ----------
    profile:
        Perfil já calculado. Quando omitido, é gerado a partir dos parâmetros.
    r2, k, turns, samples:
        Parâmetros usados apenas quando ``profile`` é ``None``.
    output:
        Caminho opcional para salvar a figura (PNG, SVG, PDF etc.).
    dpi:
        Resolução usada ao salvar a figura.
    show:
        Se ``True``, abre a janela interativa do matplotlib.
    title:
        Título do gráfico.

    Returns
    -------
    matplotlib.figure.Figure
        Figura criada. Quando ``show=False``, a figura é fechada antes do
        retorno para liberar memória.
    """
    if profile is None:
        profile = volute_profile(r2=r2, k=k, turns=turns, samples=samples)

    fig, ax = plt.subplots(figsize=(7, 7))
    draw_volute(ax, profile, title=title)
    fig.tight_layout()

    if output is not None:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(destination, dpi=dpi)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig
