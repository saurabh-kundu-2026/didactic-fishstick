from __future__ import annotations

import ast
import math
from typing import Literal, Union

Number = Union[int, float]
FlowType = Literal["counterflow", "parallelflow"]


def add(a: Number, b: Number) -> Number:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Return the difference of two numbers."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Return the product of two numbers."""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Return the quotient of two numbers.

    Raises:
        ValueError: if b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def heat_duty(m_dot: float, cp: float, delta_t: float) -> float:
    """Calculate thermal duty in watts.

    Args:
        m_dot: mass flow rate in kg/s.
        cp: specific heat in J/(kg*K).
        delta_t: temperature difference in K.
    """
    return m_dot * cp * delta_t


def log_mean_temperature_difference(delta_t1: float, delta_t2: float) -> float:
    """Return the log-mean temperature difference (LMTD)."""
    if delta_t1 <= 0 or delta_t2 <= 0:
        raise ValueError("Temperature differences must be positive.")
    if math.isclose(delta_t1, delta_t2, rel_tol=1e-12):
        return float(delta_t1)
    return (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)


def heat_exchanger_area(heat_duty_value: float, overall_heat_transfer_coefficient: float, lmtd: float) -> float:
    """Calculate required heat transfer area in square meters."""
    if overall_heat_transfer_coefficient <= 0:
        raise ValueError("Overall heat transfer coefficient must be positive.")
    if lmtd <= 0:
        raise ValueError("LMTD must be positive.")
    return heat_duty_value / (overall_heat_transfer_coefficient * lmtd)


def heat_exchanger_size(
    m_dot_hot: float,
    cp_hot: float,
    t_hot_in: float,
    t_hot_out: float,
    m_dot_cold: float,
    cp_cold: float,
    t_cold_in: float,
    t_cold_out: float,
    overall_heat_transfer_coefficient: float,
    flow_type: FlowType = "counterflow",
) -> dict[str, float]:
    """Size a simple heat exchanger for a given hot and cold stream."""
    q_hot = heat_duty(m_dot_hot, cp_hot, t_hot_in - t_hot_out)
    q_cold = heat_duty(m_dot_cold, cp_cold, t_cold_out - t_cold_in)
    if not math.isclose(q_hot, q_cold, rel_tol=1e-6, abs_tol=1e-6):
        raise ValueError("Hot and cold duties must match for the heat exchanger.")

    if flow_type == "counterflow":
        delta_t1 = t_hot_in - t_cold_out
        delta_t2 = t_hot_out - t_cold_in
    elif flow_type == "parallelflow":
        delta_t1 = t_hot_in - t_cold_in
        delta_t2 = t_hot_out - t_cold_out
    else:
        raise ValueError("flow_type must be either 'counterflow' or 'parallelflow'.")

    lmtd_value = log_mean_temperature_difference(delta_t1, delta_t2)
    area = heat_exchanger_area(q_hot, overall_heat_transfer_coefficient, lmtd_value)

    return {
        "heat_duty": q_hot,
        "lmtd": lmtd_value,
        "area": area,
        "flow_type": flow_type,
    }


def pipe_cross_sectional_area(diameter: float) -> float:
    """Return the cross-sectional area of a pipe in square meters."""
    if diameter <= 0:
        raise ValueError("Diameter must be positive.")
    return math.pi * diameter ** 2 / 4


def pipe_diameter(volumetric_flow_rate: float, velocity: float) -> float:
    """Calculate internal pipe diameter in meters from flow rate and velocity."""
    if volumetric_flow_rate <= 0:
        raise ValueError("Volumetric flow rate must be positive.")
    if velocity <= 0:
        raise ValueError("Velocity must be positive.")
    return math.sqrt(4 * volumetric_flow_rate / (math.pi * velocity))


def pump_power(flow_rate: float, head: float, density: float = 1000.0, efficiency: float = 0.7) -> float:
    """Calculate hydraulic pump power in watts.

    Args:
        flow_rate: volumetric flow rate in m^3/s.
        head: pump head in meters.
        density: fluid density in kg/m^3.
        efficiency: pump efficiency as a decimal.
    """
    if flow_rate <= 0 or head <= 0:
        raise ValueError("Flow rate and head must be positive.")
    if efficiency <= 0 or efficiency > 1:
        raise ValueError("Efficiency must be between 0 and 1.")
    g = 9.81
    return density * g * flow_rate * head / efficiency


def pump_head(power: float, flow_rate: float, density: float = 1000.0, efficiency: float = 0.7) -> float:
    """Calculate pump head from power, flow rate, density, and efficiency."""
    if power <= 0 or flow_rate <= 0:
        raise ValueError("Power and flow rate must be positive.")
    if efficiency <= 0 or efficiency > 1:
        raise ValueError("Efficiency must be between 0 and 1.")
    g = 9.81
    return power * efficiency / (density * g * flow_rate)


def filter_face_velocity(flow_rate: float, area: float) -> float:
    """Return the filter face velocity in meters per second."""
    if area <= 0:
        raise ValueError("Filter area must be positive.")
    if flow_rate < 0:
        raise ValueError("Flow rate cannot be negative.")
    return flow_rate / area


def filter_area(flow_rate: float, face_velocity: float) -> float:
    """Return the required filter area in square meters."""
    if face_velocity <= 0:
        raise ValueError("Face velocity must be positive.")
    if flow_rate < 0:
        raise ValueError("Flow rate cannot be negative.")
    return flow_rate / face_velocity


def filter_pressure_drop(flow_rate: float, area: float, resistance_coefficient: float = 10000.0) -> float:
    """Estimate filter pressure drop in pascals using face velocity squared."""
    face_velocity = filter_face_velocity(flow_rate, area)
    if resistance_coefficient < 0:
        raise ValueError("Resistance coefficient cannot be negative.")
    return resistance_coefficient * face_velocity ** 2


def reynolds_number(velocity: float, diameter: float, density: float, viscosity: float) -> float:
    """Calculate Reynolds number for pipe flow."""
    if diameter <= 0 or viscosity <= 0:
        raise ValueError("Diameter and viscosity must be positive.")
    return density * velocity * diameter / viscosity


def darcy_friction_factor(reynolds: float, relative_roughness: float = 1e-5) -> float:
    """Return the Darcy friction factor for pipe flow."""
    if reynolds <= 0:
        raise ValueError("Reynolds number must be positive.")
    if reynolds < 2300:
        return 64.0 / reynolds

    if relative_roughness < 0:
        raise ValueError("Relative roughness cannot be negative.")

    f = 0.02
    for _ in range(20):
        f = 1.0 / (
            -2.0 * math.log10(relative_roughness / 3.7 + 2.51 / (reynolds * math.sqrt(f)))
        ) ** 2
    return f


def pipe_pressure_drop(length: float, diameter: float, velocity: float, density: float, friction_factor: float) -> float:
    """Calculate pressure drop in pascals for pipe flow."""
    if length < 0 or diameter <= 0 or density <= 0:
        raise ValueError("Length, diameter, and density must be positive.")
    if friction_factor <= 0:
        raise ValueError("Friction factor must be positive.")
    return friction_factor * (length / diameter) * 0.5 * density * velocity ** 2


def pipe_pressure_drop_from_flow(
    length: float,
    diameter: float,
    volumetric_flow_rate: float,
    density: float,
    viscosity: float,
    relative_roughness: float = 1e-5,
) -> float:
    """Calculate pipe pressure drop from flow rate, in pascals."""
    if volumetric_flow_rate < 0:
        raise ValueError("Volumetric flow rate cannot be negative.")
    area = pipe_cross_sectional_area(diameter)
    velocity = volumetric_flow_rate / area
    reynolds = reynolds_number(velocity, diameter, density, viscosity)
    friction = darcy_friction_factor(reynolds, relative_roughness)
    return pipe_pressure_drop(length, diameter, velocity, density, friction)


def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression.

    Supported operators: +, -, *, /, parentheses.
    """
    node = ast.parse(expression, mode="eval")
    return _evaluate_ast(node.body)


def _evaluate_ast(node: ast.AST) -> float:
    if isinstance(node, ast.BinOp):
        left = _evaluate_ast(node.left)
        right = _evaluate_ast(node.right)
        if isinstance(node.op, ast.Add):
            return add(left, right)
        if isinstance(node.op, ast.Sub):
            return subtract(left, right)
        if isinstance(node.op, ast.Mult):
            return multiply(left, right)
        if isinstance(node.op, ast.Div):
            return divide(left, right)
        raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_evaluate_ast(node.operand)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")
