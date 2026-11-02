"""Interface gráfica Qt (PySide6) do projeto Voluta."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from . import __version__
from .aero import BlowerDesign, design_blower
from .geometry import VoluteProfile, volute_profile
from .plots import DEFAULT_TITLE, draw_volute


def _double_spin(
    minimum: float,
    maximum: float,
    value: float,
    *,
    decimals: int = 2,
    step: float = 1.0,
    suffix: str = "",
) -> QDoubleSpinBox:
    spin = QDoubleSpinBox()
    spin.setRange(minimum, maximum)
    spin.setDecimals(decimals)
    spin.setSingleStep(step)
    spin.setValue(value)
    spin.setKeyboardTracking(False)
    if suffix:
        spin.setSuffix(suffix)
    return spin


class MainWindow(QMainWindow):
    """Janela principal com as abas de geometria e dimensionamento."""

    def __init__(self) -> None:
        super().__init__()
        self._profile: VoluteProfile | None = None
        self._design: BlowerDesign | None = None

        self.setWindowTitle("Voluta — Projeto de Sopradores Centrífugos")
        self.resize(1180, 780)
        self.setMinimumSize(900, 620)

        self._build_ui()
        self._build_menu()
        self._update_plot()
        self._calculate_design()
        self.statusBar().showMessage("Pronto")

    # ------------------------------------------------------------------ UI
    def _build_ui(self) -> None:
        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 14, 18, 12)
        root.setSpacing(10)

        title = QLabel("Voluta")
        title.setStyleSheet("font-size: 26px; font-weight: 700; color: #16324f;")
        subtitle = QLabel("Geometria e dimensionamento de sopradores centrífugos")
        subtitle.setStyleSheet("color: #5b6b7c; font-size: 13px;")
        root.addWidget(title)
        root.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.addTab(self._build_geometry_tab(), "Geometria da voluta")
        tabs.addTab(self._build_design_tab(), "Dimensionamento")
        root.addWidget(tabs, 1)

        self.setCentralWidget(central)

    def _build_geometry_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)

        controls = QGroupBox("Parâmetros geométricos")
        form = QFormLayout(controls)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.geometry_r2 = _double_spin(1.0, 10_000.0, 100.0, step=5.0, suffix=" mm")
        self.geometry_k = _double_spin(0.0, 5_000.0, 25.0, step=1.0, suffix=" mm/volta")
        self.geometry_turns = _double_spin(0.1, 20.0, 1.5, step=0.1, suffix=" voltas")
        self.geometry_samples = QSpinBox()
        self.geometry_samples.setRange(2, 20_000)
        self.geometry_samples.setSingleStep(100)
        self.geometry_samples.setValue(1000)

        form.addRow("Raio externo R₂:", self.geometry_r2)
        form.addRow("Expansão K:", self.geometry_k)
        form.addRow("Voltas:", self.geometry_turns)
        form.addRow("Pontos do perfil:", self.geometry_samples)

        self.geometry_info = QLabel("—")
        self.geometry_info.setWordWrap(True)
        self.geometry_info.setStyleSheet("color: #36536b;")
        form.addRow("Resultado:", self.geometry_info)

        update_button = QPushButton("Atualizar gráfico")
        update_button.clicked.connect(self._update_plot)
        save_button = QPushButton("Salvar imagem...")
        save_button.clicked.connect(self._save_geometry_image)
        form.addRow(update_button)
        form.addRow(save_button)

        for widget in (
            self.geometry_r2,
            self.geometry_k,
            self.geometry_turns,
            self.geometry_samples,
        ):
            widget.valueChanged.connect(self._update_plot)

        self.geometry_figure = Figure(figsize=(6.2, 6.2), layout="constrained")
        self.geometry_canvas = FigureCanvasQTAgg(self.geometry_figure)
        self.geometry_ax = self.geometry_figure.add_subplot(111)

        layout.addWidget(controls, 0)
        layout.addWidget(self.geometry_canvas, 1)
        return tab

    def _build_design_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)

        inputs = QGroupBox("Entradas de projeto")
        form = QFormLayout(inputs)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.design_flow = _double_spin(0.001, 1_000.0, 0.5, decimals=4, step=0.05, suffix=" m³/s")
        self.design_pressure = _double_spin(
            1.0, 10_000_000.0, 1200.0, decimals=1, step=50.0, suffix=" Pa"
        )
        self.design_rpm = _double_spin(
            1.0, 100_000.0, 3000.0, decimals=0, step=100.0, suffix=" RPM"
        )
        self.design_rho = _double_spin(0.5, 2.0, 1.2, decimals=3, step=0.01, suffix=" kg/m³")
        self.design_psi = _double_spin(0.05, 1.5, 0.6, decimals=2, step=0.05)
        self.design_inlet_velocity = _double_spin(
            1.0, 100.0, 20.0, decimals=1, step=1.0, suffix=" m/s"
        )
        self.design_efficiency = _double_spin(0.05, 1.0, 0.70, decimals=2, step=0.01)

        form.addRow("Vazão Q:", self.design_flow)
        form.addRow("Elevação de pressão ΔP:", self.design_pressure)
        form.addRow("Rotação N:", self.design_rpm)
        form.addRow("Massa específica ρ:", self.design_rho)  # noqa: RUF001
        form.addRow("Coeficiente de pressão ψ:", self.design_psi)
        form.addRow("Velocidade de entrada C₁m:", self.design_inlet_velocity)
        form.addRow("Eficiência η:", self.design_efficiency)

        calculate_button = QPushButton("Calcular dimensionamento")
        calculate_button.setDefault(True)
        calculate_button.clicked.connect(self._calculate_design)
        export_button = QPushButton("Exportar JSON...")
        export_button.clicked.connect(self._save_design_json)
        form.addRow(calculate_button)
        form.addRow(export_button)

        results = QGroupBox("Resultados")
        results_form = QFormLayout(results)
        self.design_results: dict[str, QLabel] = {}
        for key, label in (
            ("tip_speed", "Velocidade periférica U₂:"),
            ("outlet_diameter", "Diâmetro de saída D₂:"),
            ("inlet_diameter", "Diâmetro de entrada D₁:"),
            ("shaft_power", "Potência no eixo:"),
        ):
            value = QLabel("—")
            value.setStyleSheet("font-weight: 600; color: #16324f;")
            self.design_results[key] = value
            results_form.addRow(label, value)

        note = QLabel(
            "Cálculo preliminar. Verifique perdas, curvas reais do rotor, "
            "seleção de motor e resistência mecânica."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #6b7a89; font-size: 11px;")
        results_form.addRow(note)

        layout.addWidget(inputs, 0)
        layout.addWidget(results, 1)
        return tab

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("&Arquivo")

        save_action = QAction("Salvar imagem...", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self._save_geometry_image)
        file_menu.addAction(save_action)

        export_action = QAction("Exportar dimensionamento...", self)
        export_action.triggered.connect(self._save_design_json)
        file_menu.addAction(export_action)

        file_menu.addSeparator()
        quit_action = QAction("Sair", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        help_menu = self.menuBar().addMenu("A&juda")
        about_action = QAction("Sobre o Voluta", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    # -------------------------------------------------------------- Ações
    def _update_plot(self) -> None:
        try:
            profile = volute_profile(
                r2=self.geometry_r2.value(),
                k=self.geometry_k.value(),
                turns=self.geometry_turns.value(),
                samples=self.geometry_samples.value(),
            )
        except (TypeError, ValueError) as exc:
            self.statusBar().showMessage(f"Erro: {exc}")
            return

        self._profile = profile
        draw_volute(self.geometry_ax, profile, title=DEFAULT_TITLE)
        self.geometry_canvas.draw_idle()
        self.geometry_info.setText(
            f"Raio final: {profile.outlet_radius:.2f} mm · "
            f"{profile.turns:.2f} voltas · {len(profile.theta)} pontos"
        )
        self.statusBar().showMessage("Perfil atualizado")

    def _calculate_design(self) -> None:
        try:
            design = design_blower(
                flow_rate_m3_s=self.design_flow.value(),
                pressure_rise_pa=self.design_pressure.value(),
                rpm=self.design_rpm.value(),
                rho=self.design_rho.value(),
                pressure_coefficient=self.design_psi.value(),
                inlet_velocity_m_s=self.design_inlet_velocity.value(),
                efficiency=self.design_efficiency.value(),
            )
        except (TypeError, ValueError) as exc:
            QMessageBox.warning(self, "Valores inválidos", str(exc))
            return

        self._design = design
        self.design_results["tip_speed"].setText(f"{design.tip_speed_m_s:.2f} m/s")
        self.design_results["outlet_diameter"].setText(f"{design.outlet_diameter_mm:.1f} mm")
        self.design_results["inlet_diameter"].setText(f"{design.inlet_diameter_mm:.1f} mm")
        self.design_results["shaft_power"].setText(f"{design.shaft_power_kw:.3f} kW")
        self.statusBar().showMessage("Dimensionamento atualizado")

    def _save_geometry_image(self) -> None:
        if self._profile is None:
            self._update_plot()
        if self._profile is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar imagem da voluta",
            "voluta.png",
            "PNG (*.png);;SVG (*.svg);;PDF (*.pdf);;Todos os arquivos (*)",
        )
        if not path:
            return

        try:
            self.geometry_figure.savefig(path, dpi=150, bbox_inches="tight")
        except OSError as exc:
            QMessageBox.critical(self, "Erro ao salvar", str(exc))
            return
        self.statusBar().showMessage(f"Imagem salva em {path}")

    def _save_design_json(self) -> None:
        if self._design is None:
            self._calculate_design()
        if self._design is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar dimensionamento",
            "dimensionamento.json",
            "JSON (*.json);;Todos os arquivos (*)",
        )
        if not path:
            return

        try:
            Path(path).write_text(
                json.dumps(self._design.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as exc:
            QMessageBox.critical(self, "Erro ao salvar", str(exc))
            return
        self.statusBar().showMessage(f"Dimensionamento salvo em {path}")

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "Sobre o Voluta",
            (
                f"<h2>Voluta {__version__}</h2>"
                "<p>Geometria e dimensionamento de sopradores centrífugos.</p>"
                "<p>Interface construída com PySide6 (Qt) e matplotlib.</p>"
                '<p><a href="https://github.com/dionarley/voluta">'
                "github.com/dionarley/voluta</a></p>"
            ),
        )


def run(*, smoke_test: bool = False) -> int:
    """Abre a interface gráfica e retorna o código de saída do Qt."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([sys.argv[0]])

    app.setApplicationName("Voluta")
    app.setApplicationDisplayName("Voluta")
    app.setOrganizationName("Dionarley")
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    if smoke_test:
        QTimer.singleShot(200, app.quit)

    return app.exec()


__all__ = ["MainWindow", "run"]
