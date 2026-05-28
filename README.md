# didactic-fishstick

A lightweight Python engineering calculator package with support for:

- general arithmetic evaluation
- heat exchanger sizing
- line sizing and pipe hydraulics
- pump sizing
- filter sizing and pressure-drop estimation
- a simple Tkinter GUI (when a graphical display is available)

## Project structure

- `pyproject.toml` — package metadata and build configuration
- `src/didactic_fishstick` — Python package source code
- `tests` — automated test suite
- `.gitignore` — ignored Python and environment files

## Quick start

Install the package and run tests:

```bash
python -m pip install -U pip
python -m pip install .
python -m pytest
```

## Package usage

### CLI calculator

Evaluate arithmetic expressions from the command line:

```bash
python -m didactic_fishstick calc "1 + 2 * 3"
```

Dedicated CLI sizing commands:

```bash
python -m didactic_fishstick heat --m-dot-hot 1.0 --cp-hot 4180.0 --t-hot-in 120.0 --t-hot-out 80.0 --m-dot-cold 1.0 --cp-cold 4180.0 --t-cold-in 40.0 --t-cold-out 80.0 --u 500.0 --flow-type counterflow
python -m didactic_fishstick line --flow-rate 0.01 --velocity 2.0
python -m didactic_fishstick pump power --flow-rate 0.01 --head 10.0 --efficiency 0.75
python -m didactic_fishstick pump head --power 100.0 --flow-rate 0.01 --efficiency 0.75
python -m didactic_fishstick filter area --flow-rate 0.01 --face-velocity 0.5
python -m didactic_fishstick filter pressure-drop --flow-rate 0.01 --area 0.02
python -m didactic_fishstick hydraulic --length 10.0 --diameter 0.08 --flow-rate 0.01 --viscosity 0.001
```

### GUI calculator

Launch the GUI calculator if a display server is available:

```bash
python -m didactic_fishstick gui
```

> Note: `gui` requires a graphical display. In headless environments, use the CLI mode.

### Python API examples

#### General arithmetic

```python
from didactic_fishstick import calculate

print(calculate("1 + 2 * (3 + 4)"))
```

#### Heat exchanger sizing

```python
from didactic_fishstick import heat_exchanger_size

result = heat_exchanger_size(
    m_dot_hot=1.0,
    cp_hot=4180.0,
    t_hot_in=120.0,
    t_hot_out=80.0,
    m_dot_cold=1.0,
    cp_cold=4180.0,
    t_cold_in=40.0,
    t_cold_out=80.0,
    overall_heat_transfer_coefficient=500.0,
    flow_type="counterflow",
)
print(result)
```

#### Line sizing

```python
from didactic_fishstick import pipe_diameter, pipe_cross_sectional_area

flow_rate = 0.01  # m^3/s
velocity = 2.0    # m/s

diameter = pipe_diameter(flow_rate, velocity)
area = pipe_cross_sectional_area(diameter)
print(f"Diameter: {diameter:.4f} m, Area: {area:.6f} m^2")
```

#### Pump sizing

```python
from didactic_fishstick import pump_power, pump_head

power = pump_power(flow_rate=0.01, head=10.0, density=1000.0, efficiency=0.75)
head = pump_head(power, flow_rate=0.01, density=1000.0, efficiency=0.75)
print(f"Power: {power:.0f} W, Head: {head:.1f} m")
```

#### Filter calculations

```python
from didactic_fishstick import filter_area, filter_pressure_drop

area = filter_area(0.01, face_velocity=0.5)
pressure_drop = filter_pressure_drop(0.01, area)
print(f"Filter area: {area:.3f} m^2, Pressure drop: {pressure_drop:.1f} Pa")
```

#### Hydraulic calculations

```python
from didactic_fishstick import pipe_pressure_drop_from_flow

pressure_drop = pipe_pressure_drop_from_flow(
    length=10.0,
    diameter=0.08,
    volumetric_flow_rate=0.01,
    density=1000.0,
    viscosity=0.001,
)
print(f"Pressure drop: {pressure_drop:.1f} Pa")
```

## Available calculations

- `calculate(expression)` — evaluate arithmetic expressions
- `heat_duty(m_dot, cp, delta_t)` — compute heat duty
- `log_mean_temperature_difference(delta_t1, delta_t2)` — LMTD
- `heat_exchanger_area(q, U, lmtd)` — required exchanger area
- `heat_exchanger_size(...)` — simple heat exchanger sizing
- `pipe_diameter(flow_rate, velocity)` — line sizing
- `pipe_cross_sectional_area(diameter)` — internal pipe area
- `pump_power(flow_rate, head, density, efficiency)` — pump power
- `pump_head(power, flow_rate, density, efficiency)` — pump head
- `filter_area(flow_rate, face_velocity)` — filter media area
- `filter_face_velocity(flow_rate, area)` — face velocity
- `filter_pressure_drop(flow_rate, area, resistance_coefficient)` — filter pressure drop
- `reynolds_number(velocity, diameter, density, viscosity)` — flow regime
- `darcy_friction_factor(reynolds, relative_roughness)` — friction factor
- `pipe_pressure_drop(length, diameter, velocity, density, friction_factor)` — pressure drop
- `pipe_pressure_drop_from_flow(...)` — pressure drop from flow rate

## Notes

- This package is intended as a foundation for educational and preliminary engineering calculations.
- Always validate design results with appropriate standards and engineering judgement.
