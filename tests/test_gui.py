"""Testes da interface gráfica Qt."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from voluta.gui import MainWindow


@pytest.fixture(scope="module")
def app() -> QApplication:
    application = QApplication.instance()
    if application is None:
        application = QApplication([])
    return application


def test_main_window_builds(app: QApplication) -> None:
    window = MainWindow()

    assert "Voluta" in window.windowTitle()
    assert window.geometry_r2.value() == pytest.approx(100.0)
    assert window.design_flow.value() == pytest.approx(0.5)
    assert window.design_results["outlet_diameter"].text().endswith("mm")

    window.close()


def test_geometry_update_changes_profile(app: QApplication) -> None:
    window = MainWindow()
    window.geometry_r2.setValue(80.0)
    window.geometry_k.setValue(20.0)
    window._update_plot()

    assert window._profile is not None
    assert window._profile.r2 == pytest.approx(80.0)
    assert "Raio final" in window.geometry_info.text()

    window.close()


def test_design_calculation_updates_results(app: QApplication) -> None:
    window = MainWindow()
    window.design_flow.setValue(0.5)
    window.design_pressure.setValue(1200.0)
    window.design_rpm.setValue(3000.0)
    window._calculate_design()

    assert window._design is not None
    assert window.design_results["outlet_diameter"].text() == "367.6 mm"
    assert window.design_results["inlet_diameter"].text() == "178.4 mm"

    window.close()


def test_design_export_writes_json(
    app: QApplication,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    window = MainWindow()
    destination = tmp_path / "dimensionamento.json"
    monkeypatch.setattr(
        "voluta.gui.QFileDialog.getSaveFileName",
        lambda *args, **kwargs: (str(destination), "JSON (*.json)"),
    )

    window._save_design_json()

    assert destination.exists()
    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload["outlet_diameter_m"] == pytest.approx(0.36755, rel=1e-4)

    window.close()
