"""Validação de parâmetros numéricos usada pelos módulos do projeto."""

from __future__ import annotations

import math
from typing import Any


def as_float(value: Any, name: str) -> float:
    """Converte ``value`` para ``float`` e garante que seja finito.

    Parameters
    ----------
    value:
        Valor numérico a ser convertido.
    name:
        Nome do parâmetro usado nas mensagens de erro.

    Returns
    -------
    float
        Valor convertido.

    Raises
    ------
    TypeError
        Se o valor não for numérico.
    ValueError
        Se o valor não for finito.
    """
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} deve ser numérico.") from exc

    if not math.isfinite(result):
        raise ValueError(f"{name} deve ser finito.")
    return result


def positive(value: Any, name: str) -> float:
    """Converte para ``float`` e exige um valor estritamente positivo."""
    result = as_float(value, name)
    if result <= 0:
        raise ValueError(f"{name} deve ser maior que zero.")
    return result


def non_negative(value: Any, name: str) -> float:
    """Converte para ``float`` e exige um valor maior ou igual a zero."""
    result = as_float(value, name)
    if result < 0:
        raise ValueError(f"{name} não pode ser negativo.")
    return result


def positive_ratio(value: Any, name: str) -> float:
    """Valida uma razão adimensional estritamente positiva."""
    return positive(value, name)
