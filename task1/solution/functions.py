from task1.solution.strict_decorator import strict


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

@strict
def greet(name: str, uppercase: bool) -> str:
    return name.upper() if uppercase else name.lower()

@strict
def divide(x: float, y: float) -> float:
    return x / y
