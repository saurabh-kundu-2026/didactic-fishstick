import math

from didactic_fishstick.calculator import (
    heat_duty,
    heat_exchanger_area,
    heat_exchanger_size,
    log_mean_temperature_difference,
)


def test_heat_duty_calculates_correctly() -> None:
    assert heat_duty(1.0, 4.18, 20.0) == 83.6


def test_log_mean_temperature_difference_counterflow() -> None:
    lmtd = log_mean_temperature_difference(50.0, 20.0)
    assert math.isclose(lmtd, 32.74070003811874, rel_tol=1e-9)


def test_heat_exchanger_area_calculates_from_q_u_lmtd() -> None:
    area = heat_exchanger_area(41800.0, 500.0, 32.74070003811874)
    assert math.isclose(area, 2.5533968394893125, rel_tol=1e-9)


def test_heat_exchanger_size_counterflow() -> None:
    result = heat_exchanger_size(
        m_dot_hot=1.0,
        cp_hot=4.18,
        t_hot_in=120.0,
        t_hot_out=80.0,
        m_dot_cold=1.0,
        cp_cold=4.18,
        t_cold_in=40.0,
        t_cold_out=80.0,
        overall_heat_transfer_coefficient=500.0,
        flow_type="counterflow",
    )

    assert math.isclose(result["heat_duty"], 167.2, rel_tol=1e-9)
    assert math.isclose(result["area"], 0.00836, rel_tol=1e-7)
