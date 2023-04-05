import criteria
from criteria import InputType, CriteriaIronedType, CriteriaRawType
import typing
import math
import itertools

CriteriaCombination = typing.List[int]


def get_init_possible_values() -> typing.List[InputType]:
    p = [[i for i in range(1, 6)] for k in range(3)]
    return [i for i in itertools.product(*p)]


def filter_possible_values(criss: typing.List[CriteriaCombination], input_value: InputType, possible_value: typing.List[InputType], expect: typing.List[bool]):
    cri_source = criteria.get_criterias()
    ret = []
    for pv in possible_value:
        for icris in criss:
            cris = [cri_source[i](*input_value) for i in icris]
            if expect == [x(*pv) for x in cris]:
                ret.append(pv)
                break
    return ret


def filter_possible_combin(criss: typing.List[CriteriaCombination], input_value: InputType, possible_value: typing.List[InputType], expect: typing.List[bool]):
    cri_source = criteria.get_criterias()
    ret = []
    for icris in criss:
        for pv in possible_value:
            cris = [cri_source[i](*input_value) for i in icris]
            if expect == [x(*pv) for x in cris]:
                ret.append(icris)
                break
    return ret


def hash_result(result: typing.List[bool]):
    ret = 0
    for i in result:
        ret = ret * 2
        ret = (ret + 1) if i else ret
    return ret


def spread_result(cris: CriteriaCombination, possible_value: typing.List[InputType], inputv: InputType):
    cri_source = criteria.get_criterias()
    ret: typing.Dict[int, int] = dict()
    crisv = [cri_source[cri](*inputv) for cri in cris]
    for pv in possible_value:
        v = hash_result([x(*pv) for x in crisv])
        if v in ret:
            ret[v] = ret[v] + 1
        else:
            ret.setdefault(v, 1)
    return ret


def rcc_entrophy(results: typing.Dict[int, int], possible_value: typing.List[InputType]):
    tlen = len(possible_value)
    ret = 0
    for k, v in results.items():
        ret += - math.log2(v/tlen)
    return ret


def all_possible_entrophy(cris: typing.List[CriteriaCombination], possible_value: typing.List[InputType], possible_input_value: typing.List[InputType]):
    result = []
    for v in possible_input_value:
        for cri in cris:
            ent = rcc_entrophy(spread_result(
                cri, possible_value, v), possible_value)
            result.append((v, ent))
    result.sort(key=lambda x: x[1], reverse=True)
    return [i for i in result if i[1] > 0]


def print_sorted_result(result: typing.List[typing.Tuple[InputType, float]], num=5):
    for i in range(num):
        if i < len(result):
            print("%s - %f" % result[i])


def print_combination(result: typing.List[CriteriaCombination], num=5):
    for i in range(num):
        if i < len(result):
            print("%s" % result[i], end=" ")
        else:
            break
    print("")


def print_values(result: typing.List[InputType], num=5):
    for i in range(num):
        if i < len(result):
            print("%s" % result[i], end=" ")
        else:
            break
    print("")


def print_input(result: InputType):
    print("[Input] : ", end=" ")
    for i in result:
        print(i, end=" ")
    print("")


def print_expect(result: typing.List[bool]):
    print("[Result] : ", end=" ")
    for i in result:
        print("O", end=" ") if i else print("X", end=" ")
    print("")


def iterate_possible_crits_combin(possible_crits_combin: typing.List, mode: typing.Literal['classic', 'extreme', 'nightmare']) -> typing.List[CriteriaCombination]:
    if mode == 'classic':
        return [possible_crits_combin]
    elif mode == 'extreme':
        lenv = len(possible_crits_combin)
        krr = [[0, 1] for i in range(lenv)]
        ret = []
        for ik in itertools.product(*krr):
            ret.append([possible_crits_combin[i][ik[i]]
                       for i in range(len(ik))])
        return ret
    elif mode == 'nightmare':
        lenv = len(possible_crits_combin)
        perm = [i for i in range(lenv)]
        ret = []
        for ik in itertools.permutations(perm):
            ret.append([possible_crits_combin[i][ik[i]]
                       for i in range(len(ik))])
        return ret


if __name__ == "__main__":
    mode = 'classic'

    while True:
        a = input(
            "input mode:\n[0]:Classic  [1]:Extreme  [2]:Nightmare\n>>> ")
        if a == '0':
            mode = 'classic'
            break
        elif a == '1':
            mode = 'extreme'
            break
        elif a == '2':
            mode = 'nightmare'
            break

    crits_activated = []
    if mode == 'classic':
        a = input("input num of verifiers, split by \",\" :\n>>> ")
        crits_activated = [int(x) for x in a.split(',')]
    elif mode == 'extreme':
        a = input(
            "input num of verifiers, each group is separated by \",\", verifiers in the same group is separeted by \" \":\n>>> ")
        crits_activated = [[int(y) for y in x.strip().split(' ')]
                           for x in a.split(',')]
    elif mode == 'nightmare':
        a = input(
            "input num of verifiers, split by \",\" :\n>>> ")
        crits_activated = [int(x) for x in a.split(',')]

    possible_crits_combin = iterate_possible_crits_combin(
        crits_activated, mode)

    possible_value = get_init_possible_values()
    init_pv_copy = get_init_possible_values()

    sorted_result = all_possible_entrophy(
        possible_crits_combin, possible_value, init_pv_copy)

    print_sorted_result(sorted_result)

    while True:
        a = input("input the input, for instance \"145\"  :\n>>> ")
        iv = [int(a[i]) for i in range(3)]
        print_input(iv)

        a = input("input result, 0 for \"X\" and 1 for \"O\"  :\n>>> ")
        expect = []
        for k in a:
            if ['0', 'X', 'x'].count(k) > 0:
                expect.append(False)
            elif ['1', 'O', 'o'].count(k) > 0:
                expect.append(True)

        print_expect(expect)

        oldLpv = len(possible_value)
        oldLcc = len(possible_crits_combin)

        while True:
            possible_value = filter_possible_values(
                possible_crits_combin, iv, possible_value, expect)

            possible_crits_combin = filter_possible_combin(
                possible_crits_combin, iv, possible_value, expect)

            if len(possible_value) == oldLpv and len(possible_crits_combin) == oldLcc:
                break
            else:
                oldLpv = len(possible_value)
                oldLcc = len(possible_crits_combin)

        sorted_result = all_possible_entrophy(
            possible_crits_combin, possible_value, init_pv_copy)

        print("Possible verifier combination:")
        print(possible_crits_combin[:5])

        if len(sorted_result) == 0:
            print("There is no way to distinguish the following input, try any one:")
            print(possible_value)
            break
        else:
            print("Possible answers:")
            print(possible_value[:5])

            print("Suggested input, followed by entropy:")
            print_sorted_result(sorted_result)

        if len(possible_value) < 3:
            break
