from didactic_fishstick import greet


def test_greet_returns_expected_message() -> None:
    assert greet("Alice") == "Hello, Alice! Welcome to didactic-fishstick."
