import pytest

from task1.solution.functions import sum_two, greet, divide


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (0, 0, 0),
    ]
)
def test_sum_two_valid(a, b, expected):
    assert sum_two(a, b) == expected

@pytest.mark.parametrize(
    "a, b",
    [
        (1, 2.5),
        ("1", 2),
    ]
)
def test_sum_two_invalid(a, b):
    with pytest.raises(TypeError):
        sum_two(a, b)

@pytest.mark.parametrize(
    "name, uppercase, expected",
    [
        ("Alice", True, "ALICE"),
        ("Bob", False, "bob"),
    ]
)
def test_greet_valid(name, uppercase, expected):
    assert greet(name, uppercase) == expected

@pytest.mark.parametrize(
    "name, uppercase",
    [
        (123, True),
        ("Alice", "yes"),
    ]
)
def test_greet_invalid(name, uppercase):
    with pytest.raises(TypeError):
        greet(name, uppercase)

@pytest.mark.parametrize(
    "x, y, expected",
    [
        (10.0, 2.0, 5.0),
        (3.5, 1.0, 3.5),
    ]
)
def test_divide_valid(x, y, expected):
    assert divide(x, y) == expected

@pytest.mark.parametrize(
    "x, y",
    [
        (10, "2"),
        ("3.5", 1.0),
    ]
)
def test_divide_invalid(x, y):
    with pytest.raises(TypeError):
        divide(x, y)
