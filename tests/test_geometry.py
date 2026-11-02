"""Testes da geometria da voluta."""

from __future__ import annotations

import numpy as np
import pytest

from voluta.geometry import TWO_PI, volute_profile, volute_radius


def test_radius_at_zero_is_r2() -> None:
    assert float(volute_radius(0.0, r2=100.0, k=25.0)) == pytest.approx(100.0)


def test_radius_after_one_turn_adds_k() -> None:
    assert float(volute_radius(TWO_PI, r2=100.0, k=25.0)) == pytest.approx(125.0)


def test_radius_accepts_arrays() -> None:
    theta = np.array([0.0, np.pi, TWO_PI])
    expected = np.array([100.0, 112.5, 125.0])
    np.testing.assert_allclose(volute_radius(theta, r2=100.0, k=25.0), expected)


def test_profile_has_expected_shape_and_turns() -> None:
    profile = volute_profile(r2=100.0, k=25.0, turns=1.5, samples=301)

    assert profile.x.shape == (301,)
    assert profile.y.shape == (301,)
    assert profile.turns == pytest.approx(1.5)
    assert profile.outlet_radius == pytest.approx(137.5)


def test_profile_coordinates_follow_radius() -> None:
    profile = volute_profile(r2=80.0, k=10.0, turns=1.0, samples=50)
    radius = np.hypot(profile.x, profile.y)

    np.testing.assert_allclose(radius, profile.radius)
    np.testing.assert_allclose(profile.radius, 80.0 + 10.0 * profile.theta / TWO_PI)


def test_profile_start_angle() -> None:
    profile = volute_profile(r2=100.0, k=20.0, turns=0.5, samples=10, start_angle=np.pi)

    assert profile.theta[0] == pytest.approx(np.pi)
    assert profile.x[0] == pytest.approx(-110.0)
    assert profile.y[0] == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize(
    ("kwargs", "error"),
    [
        ({"r2": 0.0}, ValueError),
        ({"r2": -1.0}, ValueError),
        ({"k": -1.0}, ValueError),
        ({"turns": 0.0}, ValueError),
        ({"samples": 1}, ValueError),
        ({"samples": 2.5}, TypeError),
        ({"start_angle": float("nan")}, ValueError),
    ],
)
def test_profile_rejects_invalid_parameters(
    kwargs: dict[str, float], error: type[Exception]
) -> None:
    with pytest.raises(error):
        volute_profile(**kwargs)


def test_radius_rejects_non_finite_angle() -> None:
    with pytest.raises(ValueError, match="finitos"):
        volute_radius(np.array([0.0, np.inf]))


def test_radius_rejects_non_numeric() -> None:
    with pytest.raises(TypeError, match="numérico"):
        volute_radius("zero")  # type: ignore[arg-type]
