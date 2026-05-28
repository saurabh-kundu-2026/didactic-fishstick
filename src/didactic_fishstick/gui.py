from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .calculator import calculate


class CalculatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Didactic Fishstick Calculator")
        self.geometry("320x240")
        self.resizable(False, False)

        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="Enter an expression and press Calculate.")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding="12")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Expression:").grid(row=0, column=0, sticky="w")
        expression_entry = ttk.Entry(frame, textvariable=self.expression_var, width=30)
        expression_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        expression_entry.focus()

        calculate_button = ttk.Button(frame, text="Calculate", command=self._on_calculate)
        calculate_button.grid(row=2, column=0, sticky="ew")

        clear_button = ttk.Button(frame, text="Clear", command=self._on_clear)
        clear_button.grid(row=2, column=1, sticky="ew", padx=(8, 0))

        result_label = ttk.Label(frame, textvariable=self.result_var, wraplength=280)
        result_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(12, 0))

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def _on_calculate(self) -> None:
        expression = self.expression_var.get().strip()
        if not expression:
            self.result_var.set("Please enter an arithmetic expression.")
            return

        try:
            result = calculate(expression)
            self.result_var.set(f"Result: {result}")
        except Exception as exc:
            self.result_var.set(f"Error: {exc}")

    def _on_clear(self) -> None:
        self.expression_var.set("")
        self.result_var.set("Enter an expression and press Calculate.")


def run() -> None:
    try:
        app = CalculatorApp()
    except tk.TclError as exc:
        raise RuntimeError(
            "Unable to open the GUI because no display is available. "
            "Run this command in an environment with a graphical display, or use the CLI mode."
        ) from exc

    app.mainloop()
