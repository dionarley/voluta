"""Geometria da voluta (carcaça espiral) de um soprador centrífugo.

A voluta é modelada pela espiral de Arquimedes. Em coordenadas polares, o
raio cresce linearmente com o ângulo polar medido a partir da língua da
voluta:

.. math::

    R(\\theta) = R_2 + K \\frac{\\theta}{2\\pi}

onde ``R2`` é o raio externo do rotor e ``K`` é a taxa de expansão da voluta
(comprimento por volta).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from ._validation import as_float, non_negative, positive

TWO_PI = 2.0 * np.pi

FloatArray = NDArray[np.float64]


@dataclass(frozen=True, eq=False)
class VoluteProfile:
    """Perfil geométrico completo de uma voluta.

    Attributes
    ----------
    theta:
        Ângulos polares em radianos.
    radius:
        Raios da voluta em milímetros (ou na unidade adotada para ``r2`` e ``k``).
    x, y:
        Coordenadas cartesianas correspondentes.
    r2:
        Raio externo do rotor.
    k:
        Taxa de expansão da voluta por volta.
    """

    theta: FloatArray
    radius: FloatArray
    x: FloatArray
    y: FloatArray
    r2: float
    k: float

    @property
    def outlet_radius(self) -> float:
        """Raio da voluta no final do traçado."""
        return float(self.radius[-1])

    @property
    def turns(self) -> float:
        """Número de voltas cobertas pelo perfil."""
        return float((self.theta[-1] - self.theta[0]) / TWO_PI)


def volute_radius(
    theta: ArrayLike,
    *,
    r2: float = 100.0,
    k: float = 25.0,
) -> FloatArray:
    """Calcula o raio da voluta em função do ângulo polar.

    Parameters
    ----------
    theta:
        Ângulo polar em radianos. Pode ser um escalar ou um array.
    r2:
        Raio externo do rotor, na mesma unidade desejada para o resultado.
    k:
        Taxa de expansão da voluta por volta (unidade de comprimento por volta).

    Returns
    -------
    numpy.ndarray
        Raio da voluta. Para uma entrada escalar, o resultado é um array 0-D.

    Raises
    ------
    ValueError
        Se ``r2`` não for positivo, ``k`` for negativo ou ``theta`` contiver
        valores não finitos.

    Examples
    --------
    >>> float(volute_radius(0.0))
    100.0
    >>> float(volute_radius(2 * np.pi))
    125.0
    """
    r2_value = positive(r2, "r2")
    k_value = non_negative(k, "k")

    try:
        theta_array = np.asarray(theta, dtype=float)
    except (TypeError, ValueError) as exc:
        raise TypeError("theta deve ser numérico.") from exc

    if not np.all(np.isfinite(theta_array)):
        raise ValueError("theta deve conter apenas valores finitos.")

    return r2_value + k_value * theta_array / TWO_PI


def volute_profile(
    *,
    r2: float = 100.0,
    k: float = 25.0,
    turns: float = 1.5,
    samples: int = 1000,
    start_angle: float = 0.0,
) -> VoluteProfile:
    """Gera o perfil cartesiano da voluta.

    Parameters
    ----------
    r2:
        Raio externo do rotor.
    k:
        Taxa de expansão da voluta por volta.
    turns:
        Número de voltas do traçado. O valor padrão, ``1.5``, reproduz o
        exemplo original do projeto.
    samples:
        Quantidade de pontos do perfil. Deve ser pelo menos 2.
    start_angle:
        Ângulo inicial em radianos.

    Returns
    -------
    VoluteProfile
        Ângulos, raios e coordenadas cartesianas do perfil.

    Examples
    --------
    >>> profile = volute_profile(turns=1.0, samples=5)
    >>> len(profile.x)
    5
    >>> profile.outlet_radius
    125.0
    """
    r2_value = positive(r2, "r2")
    k_value = non_negative(k, "k")
    turns_value = positive(turns, "turns")
    start = as_float(start_angle, "start_angle")

    if isinstance(samples, bool) or int(samples) != samples:
        raise TypeError("samples deve ser um número inteiro.")
    samples_value = int(samples)
    if samples_value < 2:
        raise ValueError("samples deve ser maior ou igual a 2.")

    theta = np.linspace(start, start + turns_value * TWO_PI, samples_value)
    radius = volute_radius(theta, r2=r2_value, k=k_value)

    return VoluteProfile(
        theta=theta,
        radius=radius,
        x=radius * np.cos(theta),
        y=radius * np.sin(theta),
        r2=r2_value,
        k=k_value,
    )
