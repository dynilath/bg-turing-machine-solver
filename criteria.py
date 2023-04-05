import typing

InputType = typing.Tuple[int, int, int]
CriteriaIronedType = typing.Callable[[int, int, int], bool]
CriteriaRawType = typing.Callable[[int, int, int], CriteriaIronedType]


def is_even(x: int):
    return x % 2 == 0


def is_odd(x: int):
    return not is_even(x)


def count_even(*args):
    return len([x for x in args if is_even(x)])


def count_value(num, *args):
    return len([x for x in args if x == num])


def same_ret(func: typing.Callable[[int, int, int], typing.Any], a: int, b: int, c: int):
    val = func(a, b, c)

    def b(a: int, b: int, c: int) -> bool:
        return func(a, b, c) == val
    return b


def map_ret(func: typing.Callable[[int, int, int], typing.List[typing.Any]], a, b, c):
    val = func(a, b, c)

    def b(a: int, b: int, c: int) -> bool:
        valn = func(a, b, c)
        return len([x for x in [0, 1, 2] if not val[x] is None and val[x] == valn[x]]) > 0
    return b


def three_way_compare(a: int, b: int):
    return 1 if a > b else -1 if a < b else 0


def gen_criteria_001_004(case, num):
    def cri(a: int, b: int, c: int):
        return same_ret(lambda a, b, c: three_way_compare(
            (a, b, c)[case], num), a, b, c)
    return cri


criteria001 = gen_criteria_001_004(0, 1)
criteria002 = gen_criteria_001_004(0, 3)
criteria003 = gen_criteria_001_004(1, 3)
criteria004 = gen_criteria_001_004(1, 4)


def gen_criteria_005_007(case):
    def cri(a: int, b: int, c: int):
        return same_ret(lambda a, b, c: is_odd((a, b, c)[case]), a, b, c)
    return cri


criteria005 = gen_criteria_005_007(0)
criteria006 = gen_criteria_005_007(1)
criteria007 = gen_criteria_005_007(2)


def gen_criteria_008_010(num):
    def cri(a: int, b: int, c: int):
        return same_ret(lambda a, b, c: count_value(num, a, b, c), a, b, c)
    return cri


criteria008 = gen_criteria_008_010(1)
criteria009 = gen_criteria_008_010(3)
criteria010 = gen_criteria_008_010(4)


def gen_criteria_011_013(case1: int, case2: int):
    def cri(a: int, b: int, c: int):
        return same_ret(lambda a, b, c: three_way_compare(
            (a, b, c)[case1], (a, b, c)[case2]), a, b, c)
    return cri


criteria011 = gen_criteria_011_013(0, 1)
criteria012 = gen_criteria_011_013(0, 2)
criteria013 = gen_criteria_011_013(1, 2)


def single_min(a, b, c):
    ar = [a, b, c]
    m = min(a, b, c)
    if ar.count(m) > 1:
        return -1
    return ar.index(m)


def single_max(a, b, c):
    ar = [a, b, c]
    m = max(a, b, c)
    if ar.count(m) > 1:
        return -1
    return ar.index(m)


def criteria014(a: int, b: int, c: int):
    return same_ret(single_min, a, b, c)


def criteria015(a: int, b: int, c: int):
    return same_ret(single_max, a, b, c)


def criteria016(a: int, b: int, c: int):
    return same_ret(lambda a, b, c: count_even(a, b, c) >= 2, a, b, c)


def criteria017(a: int, b: int, c: int):
    return same_ret(count_even, a, b, c)


def criteria018(a: int, b: int, c: int):
    return same_ret(lambda a, b, c: is_even(a+b+c), a, b, c)


def criteria019(a: int, b: int, c: int):
    return same_ret(lambda a, b, c: three_way_compare(a+b, 6), a, b, c)


def criteria020(a: int, b: int, c: int):
    def count_repeat(a, b, c):
        return 3 if a == b == c else 2 if a == b or b == c or c == a else 1
    return same_ret(count_repeat, a, b, c)


def criteria021(a: int, b: int, c: int):
    def count_pair(a, b, c):
        return 1 if a == b == c else 2 if a == b or b == c or c == a else 1
    return same_ret(count_pair, a, b, c)


def criteria022(a: int, b: int, c: int):
    def asc_dsc(a, b, c):
        return 1 if a > b > c else 2 if a < b < c else 0
    return same_ret(asc_dsc, a, b, c)


def criteria023(a: int, b: int, c: int):
    return same_ret(lambda a, b, c: three_way_compare(a+b+c, 6), a, b, c)


def criteria024(a: int, b: int, c: int):
    def asc_cnt(a, b, c):
        return 3 if a + 2 == b + 1 == c else 2 if a + 1 == b or b + 1 == c else 1
    return same_ret(asc_cnt, a, b, c)


def criteria025(a: int, b: int, c: int):
    def asc_cnt(a, b, c):
        return 3 if a + 2 == b + 1 == c else 2 if a + 1 == b or b + 1 == c else 1

    def dec_cnt(a, b, c):
        return 3 if a == b + 1 == c + 2 else 2 if a == b + 1 or b == c + 1 else 1

    val = max(asc_cnt(a, b, c), dec_cnt(a, b, c))

    def two_way(a: int, b: int, c: int):
        return max(asc_cnt(a, b, c), dec_cnt(a, b, c)) == val
    return two_way


def gen_criteria_026_033(cri: typing.Callable[[int], typing.Any]):
    def c(a: int, b: int, c: int):
        return map_ret(lambda a, b, c: list(map(cri, (a, b, c))), a, b, c)
    return c


def true_else_none(x: bool):
    return True if x else None


criteria026 = gen_criteria_026_033(lambda x:  true_else_none(x < 3))
criteria027 = gen_criteria_026_033(lambda x:  true_else_none(x < 4))
criteria028 = gen_criteria_026_033(lambda x:  true_else_none(x == 1))
criteria029 = gen_criteria_026_033(lambda x:  true_else_none(x == 3))
criteria030 = gen_criteria_026_033(lambda x:  true_else_none(x == 4))
criteria031 = gen_criteria_026_033(lambda x:  true_else_none(x > 1))
criteria032 = gen_criteria_026_033(lambda x:  true_else_none(x > 3))
criteria033 = gen_criteria_026_033(lambda x:  is_even(x))


def criteria034(a: int, b: int, c: int):
    def check(a, b, c):
        v = min(a, b, c)
        return list(map(true_else_none, (a == v, b == v, c == v)))
    return map_ret(check, a, b, c)


def criteria035(a: int, b: int, c: int):
    def check(a, b, c):
        v = max(a, b, c)
        return list(map(true_else_none, (a == v, b == v, c == v)))
    return map_ret(check, a, b, c)


def criteria036(a: int, b: int, c: int):
    def check(a, b, c):
        v = a + b + c
        return list(map(true_else_none, (v % 3 == 0, v % 4 == 0, v % 5 == 0)))
    return map_ret(check, a, b, c)


def gen_criteria_037_038(num):
    def c(a: int, b: int, c: int):
        def check(a, b, c):
            return list(map(true_else_none, (b+c == num, a + c == num, a + b == num)))
        return map_ret(check, a, b, c)
    return c


criteria037 = gen_criteria_037_038(4)
criteria038 = gen_criteria_037_038(6)

criteria039 = gen_criteria_026_033(lambda x:  three_way_compare(x, 1))
criteria040 = gen_criteria_026_033(lambda x:  three_way_compare(x, 3))
criteria041 = gen_criteria_026_033(lambda x:  three_way_compare(x, 4))


def criteria042(a: int, b: int, c: int):
    def gen_single_minmax(a, b, c):
        minid = single_min(a, b, c)
        maxid = single_max(a, b, c)

        ret = [None, None, None]
        if minid >= 0:
            ret[minid] = 1
        if maxid >= 0:
            ret[maxid] = 2
        return ret
    return map_ret(gen_single_minmax, a, b, c)


def gen_criteria_043_044(caseb: int, case1: int, case2: int):
    def gen(a: int, b: int, c: int):
        def check(a, b, c):
            r = [a, b, c]

            def sep(r, cri):
                ret = 0
                if cri(r[caseb], r[case1]):
                    ret = ret + 1
                if cri(r[caseb], r[case2]):
                    ret = ret + 2
                if ret == 0:
                    return None
                return ret
            return [sep(r, lambda a, b: a < b), sep(r, lambda a, b: a == b), sep(r, lambda a, b: a > b)]
        return map_ret(check, a, b, c)
    return gen


criteria043 = gen_criteria_043_044(0, 1, 2)
criteria044 = gen_criteria_043_044(1, 0, 2)


def gen_criteria_045_047(num1: int, num2: int):
    def gen(a: int, b: int, c: int):
        def check(a, b, c):
            r = [a, b, c]

            def sep(r: typing.List[int], cri):
                ret = 0
                if cri(r.count(num1)):
                    ret = ret + 1
                if cri(r.count(num2)):
                    ret = ret + 2
                if ret == 0:
                    return None
                return ret
            return [sep(r, lambda x: x == 0), sep(r, lambda x: x == 1), sep(r, lambda x: x == 2)]
        return map_ret(check, a, b, c)
    return gen


criteria045 = gen_criteria_045_047(1, 3)
criteria046 = gen_criteria_045_047(3, 4)
criteria047 = gen_criteria_045_047(1, 4)


def criteria048(a: int, b: int, c: int):
    return map_ret(lambda a, b, c: [three_way_compare(a, b), three_way_compare(a, c), three_way_compare(b, c)], a, b, c)


def get_criterias() -> typing.List[CriteriaRawType]:
    return [
        criteria001,
        criteria002,
        criteria003,
        criteria004,
        criteria005,
        criteria006,
        criteria007,
        criteria008,
        criteria009,
        criteria010,
        criteria011,
        criteria012,
        criteria013,
        criteria014,
        criteria015,
        criteria016,
        criteria017,
        criteria018,
        criteria019,
        criteria020,
        criteria021,
        criteria022,
        criteria023,
        criteria024,
        criteria025,
        criteria026,
        criteria027,
        criteria028,
        criteria029,
        criteria030,
        criteria031,
        criteria032,
        criteria033,
        criteria034,
        criteria035,
        criteria036,
        criteria037,
        criteria038,
        criteria039,
        criteria040,
        criteria041,
        criteria042,
        criteria043,
        criteria044,
        criteria045,
        criteria046,
        criteria047,
        criteria048,
    ]


if __name__ == "__main__":
    cris = get_criterias()

    def run_test(target: int, test: InputType, other: InputType, result=True):
        rt = cris[target-1]
        v = rt(*test)
        return v(*other) == result

    tests = [
        (1, (1, 2, 3), (1, 4, 4)),
        (1, (4, 1, 1), (4, 2, 3)),
        (1, (4, 2, 3), (1, 4, 4), False),
        (1, (1, 2, 3), (4, 4, 4), False),

        (2, (2, 2, 3), (1, 4, 4)),
        (2, (3, 2, 3), (3, 4, 4)),
        (2, (4, 2, 3), (5, 4, 4)),
        (2, (1, 2, 3), (3, 4, 4), False),
        (2, (1, 2, 3), (5, 4, 4), False),
        (2, (4, 2, 3), (3, 4, 4), False),
        (2, (5, 2, 3), (3, 4, 4), False),
        (2, (5, 2, 3), (1, 4, 4), False),

        (3, (2, 3, 3), (1, 3, 4)),
        (3, (2, 1, 3), (1, 5, 4), False),
        (3, (2, 1, 3), (1, 3, 4), False),

        (4, (2, 1, 3), (1, 2, 4)),
        (4, (2, 4, 3), (1, 4, 4)),
        (4, (2, 1, 3), (1, 4, 4), False),

        (5, (2, 1, 3), (4, 2, 4)),
        (5, (1, 1, 3), (3, 2, 4)),
        (5, (1, 1, 3), (4, 4, 4), False),

        (6, (1, 4, 3), (4, 2, 4)),
        (6, (1, 1, 3), (3, 3, 4)),
        (6, (1, 1, 3), (4, 4, 4), False),

        (7, (1, 1, 3), (4, 4, 5)),
        (7, (1, 1, 2), (4, 4, 4)),
        (7, (2, 2, 3), (4, 4, 4), False),

        (8, (1, 1, 3), (4, 1, 1)),
        (8, (2, 2, 3), (1, 4, 4), False),

        (9, (1, 1, 3), (3, 5, 1)),
        (9, (2, 2, 3), (1, 3, 3), False),

        (10, (1, 4, 3), (4, 5, 1)),
        (10, (2, 4, 4), (4, 4, 4), False),

        (11, (1, 4, 3), (3, 5, 1)),
        (11, (1, 1, 3), (5, 5, 1)),
        (11, (2, 4, 4), (4, 4, 4), False),

        (12, (1, 4, 3), (1, 5, 5)),
        (12, (2, 1, 4), (4, 1, 4), False),

        (13, (1, 4, 3), (1, 5, 2)),
        (13, (3, 1, 4), (2, 4, 2), False),

        (14, (5, 4, 3), (4, 5, 2)),
        (14, (1, 2, 1), (2, 4, 2)),
        (14, (2, 4, 2), (1, 4, 2), False),
        (14, (1, 2, 3), (2, 4, 2), False),

        (15, (5, 4, 3), (5, 1, 2)),
        (15, (1, 2, 1), (2, 4, 2)),
        (15, (4, 4, 2), (1, 4, 2), False),
        (15, (1, 2, 3), (2, 4, 2), False),

        (16, (5, 4, 3), (5, 1, 2)),
        (16, (4, 4, 2), (1, 4, 3), False),

        (17, (1, 3, 5), (1, 1, 1)),
        (17, (1, 4, 4), (4, 2, 1)),
        (17, (4, 4, 2), (1, 4, 3), False),

        (18, (1, 3, 5), (1, 1, 1)),
        (18, (2, 4, 4), (4, 1, 1)),
        (18, (4, 4, 2), (1, 4, 2), False),

        (19, (4, 2, 5), (1, 5, 1)),
        (19, (2, 1, 4), (3, 1, 1)),
        (19, (4, 4, 2), (1, 4, 2), False),

        (20, (2, 2, 2), (1, 1, 1)),
        (20, (2, 2, 2), (1, 2, 1), False),
        (20, (2, 2, 2), (1, 2, 3), False),
        (20, (1, 2, 2), (1, 1, 1), False),
        (20, (1, 2, 2), (3, 3, 2)),
        (20, (1, 2, 3), (3, 3, 1), False),

        (21, (2, 2, 2), (1, 1, 1)),
        (21, (1, 2, 3), (4, 5, 1)),
        (21, (1, 2, 2), (4, 4, 1)),
        (21, (1, 2, 2), (4, 4, 4), False),

        (22, (1, 3, 5), (2, 4, 5)),
        (22, (1, 3, 5), (5, 4, 2), False),
        (22, (4, 3, 5), (1, 4, 2)),

        (23, (1, 3, 5), (2, 4, 5)),
        (23, (1, 2, 1), (5, 4, 2), False),

        (24, (1, 2, 3), (2, 3, 4)),
        (24, (1, 3, 4), (3, 3, 4)),
        (24, (1, 3, 1), (1, 2, 4), False),
        (24, (1, 3, 4), (5, 3, 2), False),

        (25, (1, 3, 5), (2, 4, 4)),
        (25, (1, 2, 3), (2, 3, 4)),
        (25, (1, 2, 3), (4, 3, 2)),
        (25, (1, 2, 3), (2, 3, 5), False),

        (26, (2, 1, 2), (2, 5, 5)),
        (26, (5, 2, 5), (5, 1, 5)),
        (26, (5, 2, 5), (5, 3, 5), False),

        (27, (3, 1, 2), (3, 5, 5)),
        (27, (5, 3, 5), (5, 3, 5)),
        (27, (5, 3, 5), (5, 5, 5), False),

        (28, (1, 1, 5), (1, 1, 1)),
        (28, (1, 1, 1), (1, 5, 5)),
        (28, (5, 1, 5), (5, 5, 5), False),

        (29, (3, 3, 5), (3, 3, 3)),
        (29, (3, 3, 3), (3, 5, 5)),
        (29, (5, 3, 5), (5, 5, 5), False),

        (30, (4, 4, 5), (4, 4, 4)),
        (30, (4, 4, 4), (4, 5, 5)),
        (30, (5, 4, 5), (5, 5, 5), False),

        (31, (2, 2, 2), (2, 1, 1)),
        (31, (2, 1, 1), (2, 2, 2)),
        (31, (2, 1, 1), (1, 1, 1), False),

        (32, (4, 4, 4), (4, 1, 1)),
        (32, (4, 1, 1), (4, 4, 4)),
        (32, (4, 2, 1), (3, 2, 1), False),

        (33, (4, 4, 4), (4, 1, 1)),
        (33, (1, 1, 1), (4, 1, 4)),
        (33, (1, 4, 1), (4, 1, 2), False),

        (34, (3, 1, 1), (3, 2, 1)),
        (34, (1, 2, 3), (4, 4, 4)),
        (34, (1, 2, 3), (2, 3, 4)),
        (34, (1, 1, 2), (3, 2, 1), False),

        (35, (3, 3, 3), (1, 2, 3)),
        (35, (1, 2, 3), (4, 4, 4)),
        (35, (1, 2, 3), (2, 3, 4)),
        (35, (1, 2, 3), (1, 4, 1), False),
        (35, (1, 2, 3), (4, 1, 1), False),

        (36, (3, 3, 3), (4, 3, 5)),
        (36, (3, 3, 3), (4, 4, 4)),
        (36, (4, 4, 4), (1, 2, 3)),
        (36, (4, 4, 4), (2, 2, 4)),
        (36, (2, 2, 4), (4, 4, 4)),
        (36, (1, 1, 4), (4, 2, 2), False),
        (36, (5, 5, 3), (5, 4, 1), False),

        (37, (2, 2, 5), (1, 3, 5)),
        (37, (2, 2, 2), (5, 3, 1)),
        (37, (1, 3, 5), (2, 2, 2)),
        (37, (2, 2, 5), (5, 2, 2), False),
        (37, (2, 2, 5), (5, 2, 5), False),

        (38, (3, 3, 5), (2, 4, 5)),
        (38, (3, 3, 3), (5, 4, 2)),
        (38, (2, 4, 5), (3, 3, 3)),
        (38, (3, 3, 5), (5, 3, 3), False),
        (38, (3, 3, 5), (5, 3, 5), False),

        (39, (1, 1, 3), (1, 1, 4)),
        (39, (4, 4, 1), (2, 5, 1)),
        (39, (1, 1, 1), (4, 4, 4), False),
        (39, (4, 4, 4), (1, 1, 1), False),

        (40, (1, 3, 1), (5, 3, 5)),
        (40, (5, 2, 3), (2, 1, 2)),
        (40, (1, 3, 5), (5, 2, 3), False),
        (40, (3, 3, 3), (1, 4, 5), False),

        (41, (1, 4, 1), (5, 4, 5)),
        (41, (5, 2, 4), (5, 1, 5)),
        (41, (1, 4, 5), (5, 2, 3), False),
        (41, (4, 4, 4), (1, 3, 5), False),

        (42, (2, 3, 4), (1, 4, 2)),
        (42, (1, 2, 3), (2, 1, 5)),
        (42, (1, 2, 3), (4, 3, 2), False),
        (42, (4, 4, 4), (1, 3, 5), False),

        (43, (3, 2, 4), (1, 1, 2)),
        (43, (2, 4, 4), (1, 3, 2)),
        (43, (1, 2, 1), (2, 3, 1)),
        (43, (2, 2, 3), (2, 2, 2), False),

        (44, (2, 1, 3), (4, 1, 2)),
        (44, (2, 4, 2), (1, 3, 2)),
        (44, (1, 2, 3), (2, 3, 3)),
        (44, (2, 2, 3), (2, 2, 2), False),

        (45, (5, 1, 3), (1, 3, 5)),
        (45, (5, 1, 3), (3, 1, 2)),
        (45, (1, 3, 3), (1, 1, 3), False),
        (45, (1, 3, 3), (5, 5, 5), False),

        (46, (5, 4, 3), (4, 3, 5)),
        (46, (5, 4, 3), (3, 4, 2)),
        (46, (4, 3, 3), (4, 4, 3), False),
        (46, (4, 3, 3), (5, 5, 5), False),

        (47, (5, 4, 1), (4, 1, 5)),
        (47, (5, 4, 1), (1, 4, 2)),
        (47, (4, 1, 1), (4, 4, 1), False),
        (47, (4, 1, 1), (5, 5, 5), False),

        (48, (1, 2, 3), (2, 3, 4)),
        (48, (3, 3, 4), (1, 1, 5)),
        (48, (3, 2, 1), (2, 2, 2), False),
        (48, (3, 2, 1), (1, 2, 3), False),
    ]

    for i in range(len(tests)):
        t = tests[i]
        r = run_test(*t)
        print("\033[0;%s;40mRunning test criteria%03d(%03d), result = %s\033[0m" %
              ("30" if r else "31", t[0], i, "pass" if r else "error"))
