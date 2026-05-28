from didactic_fishstick import gui


def test_gui_module_imports() -> None:
    assert hasattr(gui, "run")
    assert callable(gui.run)
