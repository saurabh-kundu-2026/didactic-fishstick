"""didactic-fishstick package."""

__version__ = "0.1.0"

from .calculator import (
    add,
    calculate,
    darcy_friction_factor,
    divide,
    filter_area,
    filter_face_velocity,
    filter_pressure_drop,
    heat_duty,
    heat_exchanger_area,
    heat_exchanger_size,
    log_mean_temperature_difference,
    multiply,
    pipe_cross_sectional_area,
    pipe_diameter,
    pipe_pressure_drop,
    pipe_pressure_drop_from_flow,
    pump_head,
    pump_power,
    reynolds_number,
    subtract,
)  # noqa: F401


def greet(name: str) -> str:
    """Return a friendly greeting message."""
    return f"Hello, {name}! Welcome to didactic-fishstick."
