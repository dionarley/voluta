"""Testes da visualização da voluta."""

from __future__ import annotations

from pathlib import Path

import pytest

from voluta import plot_volute, volute_profile


def test_plot_volute_saves_png(tmp_path: Path) -> None:
    output = tmp_path / "figuras" / "voluta.png"
    fig = plot_volute(volute_profile(samples=50), output=output, dpi=80)

    assert output.exists()
    assert output.stat().st_size > 1_000
    assert fig.axes[0].get_title() == "Traçado Geométrico da Voluta de um Soprador Centrífugo"
    assert len(fig.axes[0].patches) == 1


def test_plot_volute_accepts_parameters_instead_of_profile(tmp_path: Path) -> None:
    output = tmp_path / "voluta.svg"
    plot_volute(r2=80.0, k=20.0, turns=1.0, samples=20, output=output)

    assert output.exists()
    text = output.read_text(encoding="utf-8")
    assert "<svg" in text


def test_plot_volute_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError):
        plot_volute(r2=0.0)
