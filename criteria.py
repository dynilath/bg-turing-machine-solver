import typing
from enum import Enum

InputType = typing.Tuple[int, int, int]


class Criterion:
    def __init__(self, name: str, func: typing.Callable[[InputType], bool]):
        self.name = name
        self.func = func

    def __call__(self, v: InputType):
        return self.func(v)

    def __str__(self):
        return self.name


class Color(Enum):
    BLUE = 0
    YELLOW = 1
    PURPLE = 2


def is_even(x: int):
    return x % 2 == 0


def count_even(v: InputType):
    return len([x for x in v if is_even(x)])


def count_value(num: int, v: InputType):
    return len([x for x in v if x == num])


def count_value_func(num: int, expect: int) -> typing.Callable[[InputType], bool]:
    return lambda v: len([x for x in v if x == num]) == expect


def count_value_func_list(target: int, names: typing.Tuple[str, str, str, str]):
    return list(map(lambda x: Criterion(names[x], count_value_func(target, x)), range(4)))


def gBLUE(v: InputType) -> int:
    return v[Color.BLUE.value]


def gYELLOW(v: InputType) -> int:
    return v[Color.YELLOW.value]


def gPURPLE(v: InputType) -> int:
    return v[Color.PURPLE.value]


criteria: typing.List[typing.List[Criterion]] = []

# 1. blue == 1 | blue > 1
criteria.append([Criterion("blue == 1", lambda v: gBLUE(v) == 1),
                 Criterion("blue > 1", lambda v: gBLUE(v) > 1)])


def simple_compare_func(which: Color, target: int, names: typing.List[str]):
    def f(v): return v[which.value]
    return [Criterion(names[0], lambda v: f(v) < target), Criterion(names[1], lambda v: f(v) == target), Criterion(names[2], lambda v: f(v) > target)]


# 2. blue < 3 | blue == 3 | blue > 3
criteria.append(simple_compare_func(
    Color.BLUE, 3, ["blue < 3", "blue == 3", "blue > 3"]))
# 3. yellow < 3 | yellow == 3 | yellow > 3
criteria.append(simple_compare_func(
    Color.YELLOW, 3, ["yellow < 3", "yellow == 3", "yellow > 3"]))
# 4. yellow < 4 | yellow == 4 | yellow > 4
criteria.append(simple_compare_func(
    Color.YELLOW, 4, ["yellow < 4", "yellow == 4", "yellow > 4"]))


def target_even(which: Color, names: typing.List[str]):
    def f(v): return is_even(v[which.value])
    return [Criterion(names[0], lambda v: f(v)), Criterion(names[1], lambda v: not f(v))]


# 5. blue is even | blue is odd
criteria.append(target_even(Color.BLUE, ["blue is even", "blue is odd"]))
# 6. yellow is even | yellow is odd
criteria.append(target_even(Color.YELLOW, ["yellow is even", "yellow is odd"]))
# 7. purple is even | purple is odd
criteria.append(target_even(Color.PURPLE, ["purple is even", "purple is odd"]))


# 8. 0 of 1s | 1 of 1s | 2 of 1s | 3 of 1s
criteria.append(count_value_func_list(
    1, ["0 of 1s", "1 of 1s", "2 of 1s", "3 of 1s"]))
# 9. 0 of 3s | 1 of 3s | 2 of 3s | 3 of 3s
criteria.append(count_value_func_list(
    3, ["0 of 3s", "1 of 3s", "2 of 3s", "3 of 3s"]))
# 10. 0 of 4s | 1 of 4s | 2 of 4s | 3 of 4s
criteria.append(count_value_func_list(
    4, ["0 of 4s", "1 of 4s", "2 of 4s", "3 of 4s"]))


def compare_two_func_list(target1: Color, target2: Color, names: typing.List[str]) -> typing.List[Criterion]:
    def f(v): return v[target1.value] - v[target2.value]
    return [Criterion(names[0], lambda v: f(v) < 0), Criterion(names[1], lambda v: f(v) == 0), Criterion(names[2], lambda v: f(v) > 0)]


# 11. blue < yellow | blue == yellow | blue > yellow
criteria.append(compare_two_func_list(Color.BLUE, Color.YELLOW, [
    "blue < yellow", "blue == yellow", "blue > yellow"]))
# 12. blue < purple | blue == purple | blue > purple
criteria.append(compare_two_func_list(Color.BLUE, Color.PURPLE, [
    "blue < purple", "blue == purple", "blue > purple"]))
# 13. yellow < purple | yellow == purple | yellow > purple
criteria.append(compare_two_func_list(Color.YELLOW, Color.PURPLE, [
    "yellow < purple", "yellow == purple", "yellow > purple"]))


def is_smallest(target: Color, v: InputType):
    return v[target.value] == min(v)


def is_only_smallest(target: Color, v: InputType):
    return is_smallest(target, v) and len([x for x in v if x == min(v)]) == 1


# 14. blue is only smallest | yellow is only smallest | purple is only smallest
criteria.append([Criterion("blue is only smallest", lambda v: is_only_smallest(Color.BLUE, v)),
                 Criterion("yellow is only smallest",
                           lambda v: is_only_smallest(Color.YELLOW, v)),
                 Criterion("purple is only smallest", lambda v: is_only_smallest(Color.PURPLE, v))])


def is_largest(target: Color, v: InputType):
    return v[target.value] == max(v)


def is_only_largest(target: Color, v: InputType):
    return is_largest(target.value, v) and len([x for x in v if x == max(v)]) == 1


# 15. blue is only largest | yellow is only largest | purple is only largest
criteria.append([Criterion("blue is only largest", lambda v: is_only_largest(Color.BLUE, v)),
                 Criterion("yellow is only largest",
                           lambda v: is_only_largest(Color.YELLOW, v)),
                 Criterion("purple is only largest", lambda v: is_only_largest(Color.PURPLE, v))])

# 16. even > odd | event < odd
criteria.append([Criterion("even > odd", lambda v: count_even(v) > 1),
                 Criterion("even < odd", lambda v: count_even(v) <= 1)])
# 17. 0 of even | 1 of even | 2 of even | 3 of even
criteria.append([Criterion("0 of even", lambda v: count_even(v) == 0),
                 Criterion("1 of even", lambda v: count_even(v) == 1),
                 Criterion("2 of even", lambda v: count_even(v) == 2),
                 Criterion("3 of even", lambda v: count_even(v) == 3)])
# 18. sum is even | sum is odd
criteria.append([Criterion("sum is even", lambda v: sum(v) % 2 == 0),
                 Criterion("sum is odd", lambda v: sum(v) % 2 == 1)])

# 19. blue + yellow < 6 | blue + yellow == 6 | blue + yellow > 6
criteria.append([Criterion("blue + yellow < 6", lambda v: gBLUE(v) + gYELLOW(v) < 6),
                 Criterion("blue + yellow == 6",
                           lambda v: gBLUE(v) + gYELLOW(v) == 6),
                 Criterion("blue + yellow > 6", lambda v: gBLUE(v) + gYELLOW(v) > 6)])
# 20. repeats 3 times | repeats 2 times | no repeats
criteria.append([Criterion("repeats 3 times", lambda v: len(set(v)) == 1),
                 Criterion("repeats 2 times",
                           lambda v: len(set(v)) == 2),
                 Criterion("no repeats", lambda v: len(set(v)) == 3)])
# 21. no pairs | 1 pair
criteria.append([Criterion("no pairs", lambda v: len(set(v)) == 3),
                 Criterion("1 pair", lambda v: len(set(v)) == 2)])


def in_full_ascend(v: InputType):
    return gBLUE(v) < gYELLOW(v) < gPURPLE(v)


def in_full_descend(v: InputType):
    return gBLUE(v) > gYELLOW(v) > gPURPLE(v)


def in_part_ascend(v: InputType):
    return gBLUE(v) < gYELLOW(v) or gYELLOW(v) < gPURPLE(v)


def in_part_descend(v: InputType):
    return gBLUE(v) > gYELLOW(v) or gYELLOW(v) > gPURPLE(v)


# 22. ascending | descending | no order
criteria.append([Criterion("ascending", lambda v: in_full_ascend(v)),
                 Criterion("descending", lambda v: in_full_descend(v)),
                 Criterion("no order", lambda v: not (in_full_ascend(v) or in_full_descend(v)))])
# 23. sum < 6 | sum == 6 | sum > 6
criteria.append([Criterion("sum < 6", lambda v: sum(v) < 6),
                 Criterion("sum == 6", lambda v: sum(v) == 6),
                 Criterion("sum > 6", lambda v: sum(v) > 6)])
# 24. 3 ascending | 2 ascending | no ascending
criteria.append([Criterion("3 ascending", lambda v: in_full_ascend(v)),
                 Criterion("2 ascending", lambda v: in_part_ascend(v)),
                 Criterion("no ascending", lambda v: not (in_full_ascend(v) or in_part_ascend(v)))])
# 25. no ascending or descending | 2 ascending or descending | 3 ascending or descending
criteria.append([Criterion("no ascending or descending", lambda v: not (in_full_ascend(v) or in_full_descend(v))),
                 Criterion("2 ascending or descending",
                           lambda v: in_part_ascend(v) or in_part_descend(v)),
                 Criterion("3 ascending or descending", lambda v: in_full_ascend(v) or in_full_descend(v))])


def single_test_func_list(test: typing.Callable[[int], bool], names: typing.List[str]):
    return [Criterion(names[0], lambda v: test(gBLUE(v))),
            Criterion(names[1], lambda v: test(gYELLOW(v))),
            Criterion(names[2], lambda v: test(gPURPLE(v)))]


# 26. blue < 3 | yellow < 3 | purple < 3
criteria.append(single_test_func_list(lambda x: x < 3, [
                "blue < 3", "yellow < 3", "purple < 3"]))
# 27. blue < 4 | yellow < 4 | purple < 4
criteria.append(single_test_func_list(lambda x: x < 4, [
                "blue < 4", "yellow < 4", "purple < 4"]))
# 28. blue == 1 | yellow == 1 | purple == 1
criteria.append(single_test_func_list(lambda x: x == 1, [
                "blue == 1", "yellow == 1", "purple == 1"]))
# 29. blue == 3 | yellow == 3 | purple == 3
criteria.append(single_test_func_list(lambda x: x == 3, [
                "blue == 3", "yellow == 3", "purple == 3"]))
# 30. blue == 4 | yellow == 4 | purple == 4
criteria.append(single_test_func_list(lambda x: x == 4, [
                "blue == 4", "yellow == 4", "purple == 4"]))
# 31. blue > 1 | yellow > 1 | purple > 1
criteria.append(single_test_func_list(lambda x: x > 1, [
                "blue > 1", "yellow > 1", "purple > 1"]))
# 32. blue > 3 | yellow > 3 | purple > 3
criteria.append(single_test_func_list(lambda x: x > 3, [
                "blue > 3", "yellow > 3", "purple > 3"]))
# 33. blue is even | blue is odd | yellow is even | yellow is odd | purple is even | purple is odd
criteria.append([Criterion("blue is even", lambda v: is_even(gBLUE(v))),
                 Criterion("blue is odd", lambda v: not is_even(gBLUE(v))),
                 Criterion("yellow is even",
                           lambda v: is_even(gYELLOW(v))),
                 Criterion("yellow is odd",
                           lambda v: not is_even(gYELLOW(v))),
                 Criterion("purple is even",
                           lambda v: is_even(gPURPLE(v))),
                 Criterion("purple is odd", lambda v: not is_even(gPURPLE(v)))])
# 34. blue is one of smallest | yellow is one of smallest | purple is one of smallest
criteria.append([Criterion("blue is one of smallest", lambda v: is_smallest(Color.BLUE, v)),
                 Criterion("yellow is one of smallest",
                           lambda v: is_smallest(Color.YELLOW, v)),
                 Criterion("purple is one of smallest", lambda v: is_smallest(Color.PURPLE, v))])
# 35. blue is one of largest | yellow is one of largest | purple is one of largest
criteria.append([Criterion("blue is one of largest", lambda v: is_largest(Color.BLUE, v)),
                 Criterion("yellow is one of largest",
                           lambda v: is_largest(Color.YELLOW, v)),
                 Criterion("purple is one of largest", lambda v: is_largest(Color.PURPLE, v))])
# 36. sum is multiple of 3 | sum is multiple of 4 | sum is multiple of 5
criteria.append([Criterion("sum is multiple of 3", lambda v: sum(v) % 3 == 0),
                 Criterion("sum is multiple of 4", lambda v: sum(v) % 4 == 0),
                 Criterion("sum is multiple of 5", lambda v: sum(v) % 5 == 0)])
# 37. blue + yellow == 4 | blue + purple == 4 | yellow + purple == 4
criteria.append([Criterion("blue + yellow == 4", lambda v: gBLUE(v) + gYELLOW(v) == 4),
                 Criterion("blue + purple == 4",
                           lambda v: gBLUE(v) + gPURPLE(v) == 4),
                 Criterion("yellow + purple == 4", lambda v: gYELLOW(v) + gPURPLE(v) == 4)])
# 38. blue + yellow == 6 | blue + purple == 6 | yellow + purple == 6
criteria.append([Criterion("blue + yellow == 6", lambda v: gBLUE(v) + gYELLOW(v) == 6),
                 Criterion("blue + purple == 6",
                           lambda v: gBLUE(v) + gPURPLE(v) == 6),
                 Criterion("yellow + purple == 6", lambda v: gYELLOW(v) + gPURPLE(v) == 6)])
# 39. blue == 1 | blue > 1 | yellow == 1 | yellow > 1 | purple == 1 | purple > 1
criteria.append([Criterion("blue == 1", lambda v: gBLUE(v) == 1),
                 Criterion("blue > 1", lambda v: gBLUE(v) > 1),
                 Criterion("yellow == 1", lambda v: gYELLOW(v) == 1),
                 Criterion("yellow > 1", lambda v: gYELLOW(v) > 1),
                 Criterion("purple == 1", lambda v: gPURPLE(v) == 1),
                 Criterion("purple > 1", lambda v: gPURPLE(v) > 1)])
# 40. blue < 3 | blue == 3 | blue > 3 | yellow < 3 | yellow == 3 | yellow > 3 | purple < 3 | purple == 3 | purple > 3
criteria.append(simple_compare_func(Color.BLUE, 3, ["blue < 3", "blue == 3", "blue > 3"]) +
                simple_compare_func(Color.YELLOW, 3, ["yellow < 3", "yellow == 3", "yellow > 3"]) +
                simple_compare_func(Color.PURPLE, 3, ["purple < 3", "purple == 3", "purple > 3"]))
# 41. blue < 4 | blue == 4 | blue > 4 | yellow < 4 | yellow == 4 | yellow > 4 | purple < 4 | purple == 4 | purple > 4
criteria.append(simple_compare_func(Color.BLUE, 4, ["blue < 4", "blue == 4", "blue > 4"]) +
                simple_compare_func(Color.YELLOW, 4, ["yellow < 4", "yellow == 4", "yellow > 4"]) +
                simple_compare_func(Color.PURPLE, 4, ["purple < 4", "purple == 4", "purple > 4"]))
# 42. blue is smallest | blue is largest | yellow is smallest | yellow is largest | purple is smallest | purple is largest
criteria.append([Criterion("blue is smallest", lambda v: is_smallest(Color.BLUE, v)),
                 Criterion("blue is largest",
                           lambda v: is_largest(Color.BLUE, v)),
                 Criterion("yellow is smallest",
                           lambda v: is_smallest(Color.YELLOW, v)),
                 Criterion("yellow is largest",
                           lambda v: is_largest(Color.YELLOW, v)),
                 Criterion("purple is smallest",
                           lambda v: is_smallest(Color.PURPLE, v)),
                 Criterion("purple is largest", lambda v: is_largest(Color.PURPLE, v))])
# 43. blue is lesser than yellow | blue is lesser than purple | blue is equal to yellow | blue is equal to purple | blue is greater than yellow | blue is greater than purple
criteria.append([Criterion("blue is lesser than yellow", lambda v: gBLUE(v) < gYELLOW(v)),
                 Criterion("blue is lesser than purple",
                           lambda v: gBLUE(v) < gPURPLE(v)),
                 Criterion("blue is equal to yellow",
                           lambda v: gBLUE(v) == gYELLOW(v)),
                 Criterion("blue is equal to purple",
                           lambda v: gBLUE(v) == gPURPLE(v)),
                 Criterion("blue is greater than yellow",
                           lambda v: gBLUE(v) > gYELLOW(v)),
                 Criterion("blue is greater than purple", lambda v: gBLUE(v) > gPURPLE(v))])
# 44. yellow is lesser than blue | yellow is lesser than purple | yellow is equal to blue | yellow is equal to purple | yellow is greater than blue | yellow is greater than purple
criteria.append([Criterion("yellow is lesser than blue", lambda v: gYELLOW(v) < gBLUE(v)),
                 Criterion("yellow is lesser than purple",
                           lambda v: gYELLOW(v) < gPURPLE(v)),
                 Criterion("yellow is equal to blue",
                           lambda v: gYELLOW(v) == gBLUE(v)),
                 Criterion("yellow is equal to purple",
                           lambda v: gYELLOW(v) == gPURPLE(v)),
                 Criterion("yellow is greater than blue",
                           lambda v: gYELLOW(v) > gBLUE(v)),
                 Criterion("yellow is greater than purple", lambda v: gYELLOW(v) > gPURPLE(v))])
# 45. zero of 1s | zero of 3s | one of 1s | one of 3s | two of 1s | two of 3s
criteria.append([Criterion("zero of 1s", lambda v: count_value(1, v) == 0),
                 Criterion("zero of 3s", lambda v: count_value(3, v) == 0),
                 Criterion("one of 1s", lambda v: count_value(1, v) == 1),
                 Criterion("one of 3s", lambda v: count_value(3, v) == 1),
                 Criterion("two of 1s", lambda v: count_value(1, v) == 2),
                 Criterion("two of 3s", lambda v: count_value(3, v) == 2)])
# 46. zero of 3s | zero of 4s | one of 3s | one of 4s | two of 3s | two of 4s
criteria.append([Criterion("zero of 3s", lambda v: count_value(3, v) == 0),
                 Criterion("zero of 4s", lambda v: count_value(4, v) == 0),
                 Criterion("one of 3s", lambda v: count_value(3, v) == 1),
                 Criterion("one of 4s", lambda v: count_value(4, v) == 1),
                 Criterion("two of 3s", lambda v: count_value(3, v) == 2),
                 Criterion("two of 4s", lambda v: count_value(4, v) == 2)])
# 47. zero of 1s | zero of 4s | one of 1s | one of 4s | two of 1s | two of 4s
criteria.append([Criterion("zero of 1s", lambda v: count_value(1, v) == 0),
                 Criterion("zero of 4s", lambda v: count_value(4, v) == 0),
                 Criterion("one of 1s", lambda v: count_value(1, v) == 1),
                 Criterion("one of 4s", lambda v: count_value(4, v) == 1),
                 Criterion("two of 1s", lambda v: count_value(1, v) == 2),
                 Criterion("two of 4s", lambda v: count_value(4, v) == 2)])
# 48. blue < yellow | blue == yellow | blue > yellow | blue < purple | blue == purple | blue > purple | yellow < purple | yellow == purple | yellow > purple
criteria.append(compare_two_func_list(Color.BLUE, Color.YELLOW, [
    "blue < yellow", "blue == yellow", "blue > yellow"]) +
    compare_two_func_list(Color.BLUE, Color.PURPLE, [
        "blue < purple", "blue == purple", "blue > purple"]) +
    compare_two_func_list(Color.YELLOW, Color.PURPLE, [
        "yellow < purple", "yellow == purple", "yellow > purple"]))

if __name__ == "__main__":
    red = "\033[31m"
    black = "\033[30m"
    white = "\033[37m"

    def test_criteria_single(c: Criterion, input: InputType, expect: bool):
        result = c(input)
        if (result == expect):
            return True
        else:
            print("%sTest %s failed with input %s" % (red, c, str(input)))
            return False

    TestSingle = typing.Tuple[int, InputType, bool]

    def test_criteria(cNum: int, testList: typing.List[TestSingle]):
        cri_group = criteria[cNum - 1]
        allPass = True
        for i in testList:
            j = cri_group[i[0] - 1]
            allPass = allPass and test_criteria_single(j, i[1], i[2])
        if allPass:
            print("%sTest %d passed." % (black, cNum))

    test_criteria(1, [(1, (1, 2, 3), True),
                      (1, (2, 2, 3), False),
                      (2, (2, 2, 3), True),
                      (2, (1, 2, 3), False)])

    def test_compareX(x: int):
        return [(1, (x - 1, 2, 3), True),
                (1, (x, 2, 3), False),
                (2, (x - 1, 2, 3), False),
                (2, (x, 2, 3), True),
                (2, (x + 1, 2, 3), False),
                (3, (x + 1, 2, 3), True),
                (3, (x, 2, 3), False)]

    def shift(v: InputType, offset: int):
        return (v[(3 - offset) % 3], v[(4 - offset) % 3], v[(5 - offset) % 3])

    def map_shift(v: typing.List[InputType], offset: int):
        return list(map(lambda v: (v[0], shift(v[1], offset), v[2]), v))

    test_criteria(2, test_compareX(3))
    test_criteria(3, map_shift(test_compareX(3), 1))
    test_criteria(4, map_shift(test_compareX(4), 1))

    tests_even_odd = [(1, (1, 2, 3), False),
                      (1, (3, 3, 2), False),
                      (1, (2, 2, 3), True),
                      (1, (4, 3, 2), True),
                      (2, (1, 2, 3), True),
                      (2, (3, 3, 2), True),
                      (2, (2, 2, 3), False),
                      (2, (4, 3, 2), False)]

    test_criteria(5, tests_even_odd)
    test_criteria(6, map_shift(tests_even_odd, 1))
    test_criteria(7, map_shift(tests_even_odd, 2))

    print("%sTests Finished." % (white))
