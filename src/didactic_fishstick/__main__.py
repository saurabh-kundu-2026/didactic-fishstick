import argparse
import sys

from . import greet
from .calculator import (
    calculate,
    heat_exchanger_size,
    pipe_diameter,
    pump_head,
    pump_power,
    filter_area,
    filter_pressure_drop,
    pipe_pressure_drop_from_flow,
)
from .gui import run as run_gui


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m didactic_fishstick")
    subparsers = parser.add_subparsers(dest="command")

    calc_parser = subparsers.add_parser("calc", help="Evaluate an arithmetic expression")
    calc_parser.add_argument("expression", nargs="+", help="Expression to evaluate")

    subparsers.add_parser("gui", help="Launch the GUI calculator")

    heat_parser = subparsers.add_parser("heat", help="Size a heat exchanger")
    heat_parser.add_argument("--m-dot-hot", type=float, required=True)
    heat_parser.add_argument("--cp-hot", type=float, required=True)
    heat_parser.add_argument("--t-hot-in", type=float, required=True)
    heat_parser.add_argument("--t-hot-out", type=float, required=True)
    heat_parser.add_argument("--m-dot-cold", type=float, required=True)
    heat_parser.add_argument("--cp-cold", type=float, required=True)
    heat_parser.add_argument("--t-cold-in", type=float, required=True)
    heat_parser.add_argument("--t-cold-out", type=float, required=True)
    heat_parser.add_argument("--u", type=float, required=True, dest="overall_heat_transfer_coefficient")
    heat_parser.add_argument("--flow-type", choices=["counterflow", "parallelflow"], default="counterflow")

    line_parser = subparsers.add_parser("line", help="Size a pipe diameter")
    line_parser.add_argument("--flow-rate", type=float, required=True)
    line_parser.add_argument("--velocity", type=float, required=True)

    pump_parser = subparsers.add_parser("pump", help="Pump sizing commands")
    pump_subparsers = pump_parser.add_subparsers(dest="pump_command")

    pump_power_parser = pump_subparsers.add_parser("power", help="Calculate pump power")
    pump_power_parser.add_argument("--flow-rate", type=float, required=True)
    pump_power_parser.add_argument("--head", type=float, required=True)
    pump_power_parser.add_argument("--density", type=float, default=1000.0)
    pump_power_parser.add_argument("--efficiency", type=float, default=0.7)

    pump_head_parser = pump_subparsers.add_parser("head", help="Calculate pump head")
    pump_head_parser.add_argument("--power", type=float, required=True)
    pump_head_parser.add_argument("--flow-rate", type=float, required=True)
    pump_head_parser.add_argument("--density", type=float, default=1000.0)
    pump_head_parser.add_argument("--efficiency", type=float, default=0.7)

    filter_parser = subparsers.add_parser("filter", help="Filter sizing commands")
    filter_subparsers = filter_parser.add_subparsers(dest="filter_command")

    filter_area_parser = filter_subparsers.add_parser("area", help="Calculate filter area")
    filter_area_parser.add_argument("--flow-rate", type=float, required=True)
    filter_area_parser.add_argument("--face-velocity", type=float, required=True)

    filter_drop_parser = filter_subparsers.add_parser("pressure-drop", help="Calculate filter pressure drop")
    filter_drop_parser.add_argument("--flow-rate", type=float, required=True)
    filter_drop_parser.add_argument("--area", type=float, required=True)
    filter_drop_parser.add_argument("--resistance-coefficient", type=float, default=10000.0)

    hydraulic_parser = subparsers.add_parser("hydraulic", help="Hydraulic pressure drop from flow rate")
    hydraulic_parser.add_argument("--length", type=float, required=True)
    hydraulic_parser.add_argument("--diameter", type=float, required=True)
    hydraulic_parser.add_argument("--flow-rate", type=float, required=True, dest="volumetric_flow_rate")
    hydraulic_parser.add_argument("--density", type=float, default=1000.0)
    hydraulic_parser.add_argument("--viscosity", type=float, default=0.001)
    hydraulic_parser.add_argument("--roughness", type=float, default=1e-5, dest="relative_roughness")

    greet_parser = subparsers.add_parser("greet", help="Print a greeting")
    greet_parser.add_argument("name", nargs="?", default="world")

    args = parser.parse_args()

    if args.command == "calc":
        expression = " ".join(args.expression)
        print(calculate(expression))
        return

    if args.command == "gui":
        try:
            run_gui()
            return
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            print("Falling back to CLI mode. Use:", file=sys.stderr)
            print("  python -m didactic_fishstick calc \"1 + 2 * 3\"", file=sys.stderr)
            return

    if args.command == "heat":
        result = heat_exchanger_size(
            m_dot_hot=args.m_dot_hot,
            cp_hot=args.cp_hot,
            t_hot_in=args.t_hot_in,
            t_hot_out=args.t_hot_out,
            m_dot_cold=args.m_dot_cold,
            cp_cold=args.cp_cold,
            t_cold_in=args.t_cold_in,
            t_cold_out=args.t_cold_out,
            overall_heat_transfer_coefficient=args.overall_heat_transfer_coefficient,
            flow_type=args.flow_type,
        )
        print(result)
        return

    if args.command == "line":
        diameter = pipe_diameter(args.flow_rate, args.velocity)
        print(f"Pipe diameter: {diameter:.6f} m")
        return

    if args.command == "pump":
        if args.pump_command == "power":
            power = pump_power(args.flow_rate, args.head, density=args.density, efficiency=args.efficiency)
            print(f"Pump power: {power:.2f} W")
            return
        if args.pump_command == "head":
            head = pump_head(args.power, args.flow_rate, density=args.density, efficiency=args.efficiency)
            print(f"Pump head: {head:.2f} m")
            return
        parser.print_help()
        return

    if args.command == "filter":
        if args.filter_command == "area":
            area = filter_area(args.flow_rate, args.face_velocity)
            print(f"Filter area: {area:.6f} m^2")
            return
        if args.filter_command == "pressure-drop":
            drop = filter_pressure_drop(args.flow_rate, args.area, resistance_coefficient=args.resistance_coefficient)
            print(f"Filter pressure drop: {drop:.2f} Pa")
            return
        parser.print_help()
        return

    if args.command == "hydraulic":
        drop = pipe_pressure_drop_from_flow(
            length=args.length,
            diameter=args.diameter,
            volumetric_flow_rate=args.volumetric_flow_rate,
            density=args.density,
            viscosity=args.viscosity,
            relative_roughness=args.relative_roughness,
        )
        print(f"Pressure drop: {drop:.2f} Pa")
        return

    if args.command == "greet":
        print(greet(args.name))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
