import math

from didactic_fishstick import (
    darcy_friction_factor,
    filter_area,
    filter_face_velocity,
    filter_pressure_drop,
    pipe_cross_sectional_area,
    pipe_diameter,
    pipe_pressure_drop_from_flow,
    pump_head,
    pump_power,
    reynolds_number,
)


def test_pipe_diameter_from_flow_rate() -> None:
    diameter = pipe_diameter(0.01, 2.0)
    assert math.isclose(diameter, 0.0797884560802866, rel_tol=1e-9)


def test_pipe_cross_sectional_area() -> None:
    area = pipe_cross_sectional_area(0.08)
    assert math.isclose(area, 0.005026548245743669, rel_tol=1e-9)


def test_pump_power_and_head_are_inverse() -> None:
    power = pump_power(0.01, 10.0, density=1000.0, efficiency=0.7)
    head = pump_head(power, 0.01, density=1000.0, efficiency=0.7)
    assert math.isclose(head, 10.0, rel_tol=1e-9)


def test_filter_area_and_pressure_drop() -> None:
    area = filter_area(0.01, 0.5)
    assert math.isclose(area, 0.02, rel_tol=1e-9)
    pressure_drop = filter_pressure_drop(0.01, 0.02, resistance_coefficient=10000.0)
    assert math.isclose(pressure_drop, 2500.0, rel_tol=1e-9)


def test_reynolds_and_friction_factor() -> None:
    reynolds = reynolds_number(2.0, 0.08, 1000.0, 0.001)
    assert math.isclose(reynolds, 160000.0, rel_tol=1e-9)
    friction = darcy_friction_factor(reynolds, relative_roughness=1e-5)
    assert 0.01 < friction < 0.05


def test_pipe_pressure_drop_from_flow() -> None:
    pressure_drop = pipe_pressure_drop_from_flow(
        length=10.0,
        diameter=0.08,
        volumetric_flow_rate=0.01,
        density=1000.0,
        viscosity=0.001,
        relative_roughness=1e-5,
    )
    assert pressure_drop > 0
