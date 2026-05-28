import pytest

from didactic_fishstick.calculator import add, divide, multiply, subtract, calculate


def test_add_returns_sum() -> None:
    assert add(2, 3) == 5


def test_subtract_returns_difference() -> None:
    assert subtract(5, 2) == 3


def test_multiply_returns_product() -> None:
    assert multiply(4, 3) == 12


def test_divide_returns_quotient() -> None:
    assert divide(10, 2) == 5.0


def test_divide_by_zero_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)


def test_calculate_evaluates_simple_expression() -> None:
    assert calculate("1 + 2 * 3") == 7.0


def test_calculate_supports_parentheses() -> None:
    assert calculate("(1 + 2) * 3") == 9.0


def test_calculate_supports_negative_numbers() -> None:
    assert calculate("-4 + 2") == -2.0
