from task1.solution.functions import sum_two, greet, divide


def test_sum_two():
    assert sum_two(1, 2) == 3
    assert sum_two(0, 0) == 0

    try:
        sum_two(1, 2.5)
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError")

def test_greet():
    assert greet("Alice", True) == "ALICE"
    assert greet("Bob", False) == "bob"

    try:
        greet(123, True)
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError")

def test_divide():
    assert divide(10.0, 2.0) == 5.0
    assert divide(3.5, 1.0) == 3.5

    try:
        divide("10", 2)
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError")

if __name__ == "__main__":
    test_sum_two()
    test_greet()
    test_divide()
    print("Tests passed!")
