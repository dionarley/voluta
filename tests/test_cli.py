"""Testes da interface de linha de comando."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from voluta.cli import main


def test_plot_command_writes_image(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output = tmp_path / "voluta.png"

    assert main(["plot", "--output", str(output), "--samples", "40", "--dpi", "60"]) == 0
    assert output.exists()
    assert output.stat().st_size > 1_000
    assert "Figura salva em:" in capsys.readouterr().out


def test_design_command_outputs_json(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(
        [
            "design",
            "--flow",
            "0.5",
            "--pressure",
            "1200",
            "--rpm",
            "3000",
            "--json",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["outlet_diameter_m"] == pytest.approx(0.36755, rel=1e-4)
    assert payload["inlet_diameter_m"] == pytest.approx(0.17841, rel=1e-4)
    assert payload["shaft_power_kw"] == pytest.approx(0.857142857)


def test_design_command_outputs_table(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["design", "--flow", "0.5", "--pressure", "1200", "--rpm", "3000"]) == 0
    output = capsys.readouterr().out
    assert "Dimensionamento do soprador centrífugo" in output
    assert "Diâmetro de saída" in output


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
    assert "0.2.0" in capsys.readouterr().out


def test_invalid_values_exit_with_usage_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["design", "--flow", "0", "--pressure", "1200", "--rpm", "3000"])

    assert exc_info.value.code == 2
    assert "maior que zero" in capsys.readouterr().err
