from math_service.services.math_services import power, factorial, fibonacci


def test_power():
    assert power(2, 3) == 8


def test_factorial():
    assert factorial(5) == 120


def test_fibonacci():
    assert fibonacci(7) == 13
