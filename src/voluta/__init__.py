"""Voluta: geometria da carcaça, dimensionamento e visualização de sopradores.

O pacote reúne as equações do documento *Matemática dos Sopradores* em uma
API Python testável e em uma interface de linha de comando.

Examples
--------
>>> from voluta import design_blower, volute_profile
>>> profile = volute_profile(turns=1.0)
>>> profile.outlet_radius
125.0
>>> design = design_blower(0.5, 1200, 3000)
>>> round(design.outlet_diameter_mm)
368
"""

from __future__ import annotations

from .aero import (
    BlowerDesign,
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
from .geometry import VoluteProfile, volute_profile, volute_radius
from .plots import plot_volute

__version__ = "0.2.0"

__all__ = [
    "BlowerDesign",
    "VoluteProfile",
    "__version__",
    "affinity_flow",
    "affinity_power",
    "affinity_pressure",
    "blade_width",
    "design_blower",
    "euler_pressure",
    "inlet_diameter",
    "outlet_diameter",
    "peripheral_velocity",
    "plot_volute",
    "shaft_power",
    "volute_profile",
    "volute_radius",
]
