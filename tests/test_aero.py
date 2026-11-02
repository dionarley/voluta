"""Testes das equações de dimensionamento e das leis de afinidade."""

from __future__ import annotations

import math

import pytest

from voluta.aero import (
    affinity_flow,
    affinity_power,
    affinity_pressure,
    blade_width,
    design_blower,
    euler_pressure,
    inlet_diameter,
    outlet_diameter,
    peripheral_velocity,
    shaft_power,
)


def test_peripheral_velocity() -> None:
    assert peripheral_velocity(0.2, 3000.0) == pytest.approx(math.pi * 0.2 * 3000.0 / 60.0)


def test_euler_pressure_with_inlet_swirl() -> None:
    result = euler_pressure(30.0, 20.0, u1=10.0, c_u1=5.0, rho=1.2)
    assert result == pytest.approx(1.2 * (30.0 * 20.0 - 10.0 * 5.0))


def test_euler_pressure_without_inlet_swirl() -> None:
    assert euler_pressure(30.0, 20.0) == pytest.approx(720.0)


def test_outlet_diameter() -> None:
    result = outlet_diameter(1200.0, 3000.0, rho=1.2, pressure_coefficient=0.6)
    expected = 60.0 * math.sqrt(2.0 * 1200.0 / (1.2 * 0.6)) / (math.pi * 3000.0)
    assert result == pytest.approx(expected)
    assert result == pytest.approx(0.36755, rel=1e-4)


def test_inlet_diameter() -> None:
    result = inlet_diameter(0.5, 20.0)
    assert result == pytest.approx(math.sqrt(4.0 * 0.5 / (math.pi * 20.0)))
    assert result == pytest.approx(0.17841, rel=1e-4)


def test_blade_width() -> None:
    result = blade_width(0.5, 0.36755, 10.0)
    assert result == pytest.approx(0.5 / (math.pi * 0.36755 * 10.0))


def test_shaft_power() -> None:
    assert shaft_power(0.5, 1200.0, efficiency=0.7) == pytest.approx(857.142857)


def test_affinity_laws_with_speed_change() -> None:
    assert affinity_flow(1.0, speed_ratio=2.0) == pytest.approx(2.0)
    assert affinity_pressure(100.0, speed_ratio=2.0) == pytest.approx(400.0)
    assert affinity_power(1000.0, speed_ratio=2.0) == pytest.approx(8000.0)


def test_affinity_laws_with_diameter_change() -> None:
    assert affinity_flow(1.0, diameter_ratio=2.0) == pytest.approx(8.0)
    assert affinity_pressure(100.0, diameter_ratio=2.0) == pytest.approx(400.0)
    assert affinity_power(1000.0, diameter_ratio=2.0) == pytest.approx(32000.0)


def test_affinity_laws_combine_speed_and_diameter() -> None:
    assert affinity_flow(1.0, speed_ratio=2.0, diameter_ratio=2.0) == pytest.approx(16.0)
    assert affinity_pressure(100.0, speed_ratio=2.0, diameter_ratio=2.0) == pytest.approx(1600.0)
    assert affinity_power(1000.0, speed_ratio=2.0, diameter_ratio=2.0) == pytest.approx(256000.0)


def test_design_blower_combines_the_equations() -> None:
    design = design_blower(
        0.5,
        1200.0,
        3000.0,
        rho=1.2,
        pressure_coefficient=0.6,
        inlet_velocity_m_s=20.0,
        efficiency=0.7,
    )

    assert design.tip_speed_m_s == pytest.approx(math.sqrt(2.0 * 1200.0 / (1.2 * 0.6)))
    assert design.outlet_diameter_m == pytest.approx(0.36755, rel=1e-4)
    assert design.inlet_diameter_m == pytest.approx(0.17841, rel=1e-4)
    assert design.outlet_diameter_mm == pytest.approx(design.outlet_diameter_m * 1000.0)
    assert design.shaft_power_w == pytest.approx(857.142857)
    assert design.shaft_power_kw == pytest.approx(0.857142857)


def test_design_to_dict_contains_si_and_practical_units() -> None:
    payload = design_blower(0.5, 1200.0, 3000.0).to_dict()

    assert payload["outlet_diameter_mm"] == pytest.approx(payload["outlet_diameter_m"] * 1000.0)
    assert payload["inlet_diameter_mm"] == pytest.approx(payload["inlet_diameter_m"] * 1000.0)
    assert payload["shaft_power_kw"] == pytest.approx(payload["shaft_power_w"] / 1000.0)


@pytest.mark.parametrize(
    ("call", "error"),
    [
        (lambda: peripheral_velocity(0.0, 3000.0), ValueError),
        (lambda: peripheral_velocity(0.2, 0.0), ValueError),
        (lambda: euler_pressure(-1.0, 10.0), ValueError),
        (lambda: euler_pressure(30.0, 20.0, rho=0.0), ValueError),
        (lambda: outlet_diameter(0.0, 3000.0), ValueError),
        (lambda: inlet_diameter(0.5, 0.0), ValueError),
        (lambda: blade_width(-0.5, 0.2, 10.0), ValueError),
        (lambda: shaft_power(0.5, 1200.0, efficiency=1.5), ValueError),
        (lambda: affinity_flow(1.0, speed_ratio=0.0), ValueError),
        (lambda: design_blower(0.5, 1200.0, 3000.0, efficiency=0.0), ValueError),
    ],
)
def test_functions_reject_invalid_parameters(call: object, error: type[Exception]) -> None:
    with pytest.raises(error):
        call()  # type: ignore[operator]
