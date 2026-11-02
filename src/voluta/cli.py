"""Interface de linha de comando do projeto."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from importlib.metadata import PackageNotFoundError, version
from importlib.util import find_spec
from pathlib import Path

from .aero import BlowerDesign, design_blower
from .geometry import volute_profile
from .plots import plot_volute


def _package_version() -> str:
    try:
        return version("voluta")
    except PackageNotFoundError:  # execução diretamente do código-fonte
        return "0.2.1"


def build_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da CLI."""
    parser = argparse.ArgumentParser(
        prog="voluta",
        description="Geometria e dimensionamento de sopradores centrífugos.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {_package_version()}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plot_parser = subparsers.add_parser(
        "plot",
        help="Gera o traçado da voluta em uma imagem.",
        description="Gera o traçado geométrico da voluta e do rotor.",
    )
    plot_parser.add_argument("--r2", type=float, default=100.0, help="Raio externo do rotor.")
    plot_parser.add_argument("--k", type=float, default=25.0, help="Expansão da voluta por volta.")
    plot_parser.add_argument(
        "--turns", type=float, default=1.5, help="Número de voltas do traçado."
    )
    plot_parser.add_argument("--samples", type=int, default=1000, help="Pontos do perfil.")
    plot_parser.add_argument(
        "--output",
        type=Path,
        default=Path("voluta.png"),
        help="Arquivo de saída (padrão: voluta.png).",
    )
    plot_parser.add_argument("--dpi", type=int, default=150, help="Resolução da imagem.")
    plot_parser.add_argument("--title", default=None, help="Título personalizado do gráfico.")
    plot_parser.add_argument(
        "--show",
        action="store_true",
        help="Abre a janela interativa em vez de apenas salvar.",
    )

    design_parser = subparsers.add_parser(
        "design",
        help="Calcula um dimensionamento preliminar do soprador.",
        description="Calcula diâmetros, velocidade periférica e potência no eixo.",
    )
    design_parser.add_argument("--flow", type=float, required=True, help="Vazão em m³/s.")
    design_parser.add_argument(
        "--pressure",
        type=float,
        required=True,
        help="Elevação de pressão total em Pa.",
    )
    design_parser.add_argument("--rpm", type=float, required=True, help="Rotação em RPM.")
    design_parser.add_argument("--rho", type=float, default=1.2, help="Massa específica do ar.")
    design_parser.add_argument(
        "--psi",
        type=float,
        default=0.6,
        help="Coeficiente adimensional de pressão.",
    )
    design_parser.add_argument(
        "--inlet-velocity",
        type=float,
        default=20.0,
        help="Velocidade meridional na entrada em m/s.",
    )
    design_parser.add_argument(
        "--efficiency",
        type=float,
        default=0.7,
        help="Eficiência global entre 0 e 1.",
    )
    design_parser.add_argument("--json", action="store_true", help="Imprime o resultado em JSON.")

    gui_parser = subparsers.add_parser(
        "gui",
        help="Abre a interface gráfica Qt.",
        description="Abre a interface gráfica para explorar a geometria e o dimensionamento.",
    )
    gui_parser.add_argument(
        "--smoke-test",
        action="store_true",
        help=argparse.SUPPRESS,
    )

    return parser


def _format_design(design: BlowerDesign) -> str:
    return "\n".join(
        [
            "Dimensionamento do soprador centrífugo",
            "======================================",
            f"Vazão .................... {design.flow_rate_m3_s:.4f} m³/s",
            f"Elevação de pressão ...... {design.pressure_rise_pa:.1f} Pa",
            f"Rotação .................. {design.rpm:.1f} RPM",
            f"Velocidade periférica .... {design.tip_speed_m_s:.2f} m/s",
            f"Diâmetro de saída ........ {design.outlet_diameter_mm:.1f} mm",
            f"Diâmetro de entrada ...... {design.inlet_diameter_mm:.1f} mm",
            f"Potência no eixo ......... {design.shaft_power_kw:.3f} kW",
            f"Eficiência adotada ....... {design.efficiency:.2%}",
        ]
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Executa a CLI e retorna o código de saída."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "plot":
            profile = volute_profile(
                r2=args.r2,
                k=args.k,
                turns=args.turns,
                samples=args.samples,
            )
            kwargs = {}
            if args.title is not None:
                kwargs["title"] = args.title
            plot_volute(
                profile,
                output=args.output,
                dpi=args.dpi,
                show=args.show,
                **kwargs,
            )
            if not args.show:
                print(f"Figura salva em: {args.output.resolve()}")
            return 0

        if args.command == "design":
            design = design_blower(
                flow_rate_m3_s=args.flow,
                pressure_rise_pa=args.pressure,
                rpm=args.rpm,
                rho=args.rho,
                pressure_coefficient=args.psi,
                inlet_velocity_m_s=args.inlet_velocity,
                efficiency=args.efficiency,
            )
            if args.json:
                print(json.dumps(design.to_dict(), indent=2, ensure_ascii=False))
            else:
                print(_format_design(design))
            return 0

        if args.command == "gui":
            if find_spec("PySide6") is None:
                parser.error("A interface gráfica requer PySide6. Instale com: uv sync --group gui")
            try:
                from .gui import run
            except ImportError as exc:
                parser.error(
                    "Não foi possível carregar a interface gráfica Qt.\n"
                    f"Detalhe: {exc}\n"
                    "No Linux/NixOS, verifique as bibliotecas de sistema do Qt "
                    "(libGL, libxkbcommon, libxcb, libX11 e dbus)."
                )
            return run(smoke_test=args.smoke_test)
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))

    parser.error("comando não reconhecido")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
