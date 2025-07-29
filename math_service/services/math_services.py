# Build the services, business logic
from math_service.cache.simple_cache import get_from_cache, set_to_cache


def power(a: int, b: int) -> int:
    key = f"pow:{a}:{b}"
    if (cached := get_from_cache(key)) is not None:
        return cached
    result = a ** b
    set_to_cache(key, result)
    return result


def factorial(n: int) -> int:
    key = f"fact:{n}"
    if (cached := get_from_cache(key)) is not None:
        return cached
    result = 1
    for i in range(2, n + 1):
        result *= i
    set_to_cache(key, result)
    return result


def fibonacci(n: int) -> int:
    key = f"fib:{n}"
    if (cached := get_from_cache(key)) is not None:
        return cached
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    set_to_cache(key, a)
    return a
