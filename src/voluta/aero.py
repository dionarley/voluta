"""Equações de dimensionamento e escalabilidade de sopradores centrífugos.

Todas as funções usam unidades do SI: metros, segundos, pascal, watt e
rotações por minuto (RPM).
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from ._validation import as_float, non_negative, positive, positive_ratio


def peripheral_velocity(diameter_m: float, rpm: float) -> float:
    """Velocidade periférica do rotor.

    .. math::

        U = \\frac{\\pi D N}{60}

    Parameters
    ----------
    diameter_m:
        Diâmetro do rotor em metros.
    rpm:
        Rotação em rotações por minuto.

    Returns
    -------
    float
        Velocidade periférica em m/s.
    """
    diameter = positive(diameter_m, "diameter_m")
    rotation = positive(rpm, "rpm")
    return math.pi * diameter * rotation / 60.0


def euler_pressure(
    u2: float,
    c_u2: float,
    *,
    u1: float = 0.0,
    c_u1: float = 0.0,
    rho: float = 1.2,
) -> float:
    """Elevação de pressão teórica pela equação de Euler.

    .. math::

        \\Delta P_{th} = \\rho (U_2 C_{u2} - U_1 C_{u1})

    Para entrada radial sem pré-rotação, ``C_u1 = 0``.

    Parameters
    ----------
    u2, c_u2:
        Velocidade periférica e componente tangencial absoluta na saída (m/s).
    u1, c_u1:
        Velocidade periférica e componente tangencial absoluta na entrada (m/s).
    rho:
        Massa específica do ar em kg/m³.

    Returns
    -------
    float
        Elevação de pressão teórica em pascal.
    """
    u2_value = non_negative(u2, "u2")
    c_u2_value = as_float(c_u2, "c_u2")
    u1_value = non_negative(u1, "u1")
    c_u1_value = as_float(c_u1, "c_u1")
    rho_value = positive(rho, "rho")

    return rho_value * (u2_value * c_u2_value - u1_value * c_u1_value)


def outlet_diameter(
    pressure_rise_pa: float,
    rpm: float,
    *,
    rho: float = 1.2,
    pressure_coefficient: float = 0.6,
) -> float:
    """Diâmetro externo do rotor a partir do coeficiente de pressão.

    .. math::

        U_2 = \\sqrt{\\frac{2 \\Delta P_t}{\\rho \\psi}},
        \\qquad D_2 = \\frac{60 U_2}{\\pi N}

    Parameters
    ----------
    pressure_rise_pa:
        Aumento de pressão total desejado em pascal.
    rpm:
        Rotação em RPM.
    rho:
        Massa específica do ar em kg/m³.
    pressure_coefficient:
        Coeficiente adimensional de pressão :math:`\\psi`.

    Returns
    -------
    float
        Diâmetro externo do rotor em metros.
    """
    pressure = positive(pressure_rise_pa, "pressure_rise_pa")
    rotation = positive(rpm, "rpm")
    rho_value = positive(rho, "rho")
    coefficient = positive(pressure_coefficient, "pressure_coefficient")

    tip_speed = math.sqrt(2.0 * pressure / (rho_value * coefficient))
    return 60.0 * tip_speed / (math.pi * rotation)


def inlet_diameter(flow_rate_m3_s: float, inlet_velocity_m_s: float) -> float:
    """Diâmetro de entrada do rotor pela continuidade.

    .. math::

        D_1 = \\sqrt{\\frac{4Q}{\\pi C_{1m}}}

    Parameters
    ----------
    flow_rate_m3_s:
        Vazão volumétrica em m³/s.
    inlet_velocity_m_s:
        Velocidade meridional na entrada em m/s. Valores usuais ficam entre
        15 e 25 m/s.

    Returns
    -------
    float
        Diâmetro de entrada em metros.
    """
    flow = positive(flow_rate_m3_s, "flow_rate_m3_s")
    velocity = positive(inlet_velocity_m_s, "inlet_velocity_m_s")
    return math.sqrt(4.0 * flow / (math.pi * velocity))


def blade_width(
    flow_rate_m3_s: float,
    diameter_m: float,
    meridional_velocity_m_s: float,
) -> float:
    """Largura da pá em uma seção, pela conservação de massa.

    .. math::

        b = \\frac{Q}{\\pi D C_m}

    Parameters
    ----------
    flow_rate_m3_s:
        Vazão volumétrica em m³/s.
    diameter_m:
        Diâmetro da seção em metros.
    meridional_velocity_m_s:
        Componente meridional da velocidade em m/s.

    Returns
    -------
    float
        Largura da pá em metros.
    """
    flow = positive(flow_rate_m3_s, "flow_rate_m3_s")
    diameter = positive(diameter_m, "diameter_m")
    velocity = positive(meridional_velocity_m_s, "meridional_velocity_m_s")
    return flow / (math.pi * diameter * velocity)


def shaft_power(
    flow_rate_m3_s: float,
    pressure_rise_pa: float,
    *,
    efficiency: float = 0.7,
) -> float:
    """Potência mecânica no eixo considerando a eficiência global.

    .. math::

        P_{eixo} = \\frac{Q \\Delta P_t}{\\eta}

    Parameters
    ----------
    flow_rate_m3_s:
        Vazão volumétrica em m³/s.
    pressure_rise_pa:
        Aumento de pressão total em pascal.
    efficiency:
        Eficiência global entre 0 e 1.

    Returns
    -------
    float
        Potência no eixo em watt.
    """
    flow = positive(flow_rate_m3_s, "flow_rate_m3_s")
    pressure = positive(pressure_rise_pa, "pressure_rise_pa")
    eta = positive(efficiency, "efficiency")
    if eta > 1.0:
        raise ValueError("efficiency deve estar entre 0 e 1.")

    return flow * pressure / eta


def affinity_flow(
    flow_rate_m3_s: float,
    *,
    speed_ratio: float = 1.0,
    diameter_ratio: float = 1.0,
) -> float:
    """Nova vazão pelas leis de afinidade.

    .. math::

        Q_2 = Q_1 \\left(\\frac{N_2}{N_1}\\right)
        \\left(\\frac{D_2}{D_1}\\right)^3
    """
    flow = positive(flow_rate_m3_s, "flow_rate_m3_s")
    n_ratio = positive_ratio(speed_ratio, "speed_ratio")
    d_ratio = positive_ratio(diameter_ratio, "diameter_ratio")
    return flow * n_ratio * d_ratio**3


def affinity_pressure(
    pressure_rise_pa: float,
    *,
    speed_ratio: float = 1.0,
    diameter_ratio: float = 1.0,
) -> float:
    """Nova elevação de pressão pelas leis de afinidade.

    .. math::

        \\Delta P_2 = \\Delta P_1 \\left(\\frac{N_2}{N_1}\\right)^2
        \\left(\\frac{D_2}{D_1}\\right)^2
    """
    pressure = positive(pressure_rise_pa, "pressure_rise_pa")
    n_ratio = positive_ratio(speed_ratio, "speed_ratio")
    d_ratio = positive_ratio(diameter_ratio, "diameter_ratio")
    return pressure * n_ratio**2 * d_ratio**2


def affinity_power(
    power_w: float,
    *,
    speed_ratio: float = 1.0,
    diameter_ratio: float = 1.0,
) -> float:
    """Nova potência pelas leis de afinidade.

    .. math::

        P_2 = P_1 \\left(\\frac{N_2}{N_1}\\right)^3
        \\left(\\frac{D_2}{D_1}\\right)^5
    """
    power = positive(power_w, "power_w")
    n_ratio = positive_ratio(speed_ratio, "speed_ratio")
    d_ratio = positive_ratio(diameter_ratio, "diameter_ratio")
    return power * n_ratio**3 * d_ratio**5


@dataclass(frozen=True)
class BlowerDesign:
    """Resultado de um dimensionamento preliminar de soprador centrífugo."""

    flow_rate_m3_s: float
    pressure_rise_pa: float
    rpm: float
    rho_kg_m3: float
    pressure_coefficient: float
    inlet_velocity_m_s: float
    efficiency: float
    tip_speed_m_s: float
    outlet_diameter_m: float
    inlet_diameter_m: float
    shaft_power_w: float

    @property
    def outlet_diameter_mm(self) -> float:
        """Diâmetro externo do rotor em milímetros."""
        return self.outlet_diameter_m * 1_000.0

    @property
    def inlet_diameter_mm(self) -> float:
        """Diâmetro de entrada do rotor em milímetros."""
        return self.inlet_diameter_m * 1_000.0

    @property
    def shaft_power_kw(self) -> float:
        """Potência no eixo em quilowatt."""
        return self.shaft_power_w / 1_000.0

    def to_dict(self) -> dict[str, Any]:
        """Converte o resultado em um dicionário serializável em JSON."""
        result = asdict(self)
        result.update(
            outlet_diameter_mm=self.outlet_diameter_mm,
            inlet_diameter_mm=self.inlet_diameter_mm,
            shaft_power_kw=self.shaft_power_kw,
        )
        return result


def design_blower(
    flow_rate_m3_s: float,
    pressure_rise_pa: float,
    rpm: float,
    *,
    rho: float = 1.2,
    pressure_coefficient: float = 0.6,
    inlet_velocity_m_s: float = 20.0,
    efficiency: float = 0.7,
) -> BlowerDesign:
    """Dimensiona os principais parâmetros geométricos de um soprador.

    O cálculo combina o coeficiente de pressão, a continuidade na entrada e a
    potência no eixo. O resultado é preliminar e não substitui a verificação
    de perdas, resistência mecânica e curvas reais do rotor.

    Parameters
    ----------
    flow_rate_m3_s:
        Vazão volumétrica em m³/s.
    pressure_rise_pa:
        Aumento de pressão total em pascal.
    rpm:
        Rotação em RPM.
    rho:
        Massa específica do ar em kg/m³.
    pressure_coefficient:
        Coeficiente adimensional de pressão :math:`\\psi`.
    inlet_velocity_m_s:
        Velocidade meridional na entrada em m/s.
    efficiency:
        Eficiência global entre 0 e 1.

    Returns
    -------
    BlowerDesign
        Diâmetros, velocidade periférica e potência no eixo.
    """
    flow = positive(flow_rate_m3_s, "flow_rate_m3_s")
    pressure = positive(pressure_rise_pa, "pressure_rise_pa")
    rotation = positive(rpm, "rpm")
    rho_value = positive(rho, "rho")
    coefficient = positive(pressure_coefficient, "pressure_coefficient")
    inlet_velocity = positive(inlet_velocity_m_s, "inlet_velocity_m_s")
    eta = positive(efficiency, "efficiency")
    if eta > 1.0:
        raise ValueError("efficiency deve estar entre 0 e 1.")

    tip_speed = math.sqrt(2.0 * pressure / (rho_value * coefficient))
    d2 = 60.0 * tip_speed / (math.pi * rotation)
    d1 = math.sqrt(4.0 * flow / (math.pi * inlet_velocity))
    power = flow * pressure / eta

    return BlowerDesign(
        flow_rate_m3_s=flow,
        pressure_rise_pa=pressure,
        rpm=rotation,
        rho_kg_m3=rho_value,
        pressure_coefficient=coefficient,
        inlet_velocity_m_s=inlet_velocity,
        efficiency=eta,
        tip_speed_m_s=tip_speed,
        outlet_diameter_m=d2,
        inlet_diameter_m=d1,
        shaft_power_w=power,
    )
