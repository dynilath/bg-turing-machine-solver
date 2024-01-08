import typing
import math
from itertools import combinations, product

from criteria import InputType, criteria


class CriteriaEntropy:
    ResultType = typing.Tuple[float, typing.List[int], InputType]

    def __init__(self, actived_group: typing.List[int], possible_combination: typing.List[typing.Tuple[int, ...]]):
        self.groups = actived_group
        self.combinations = possible_combination
        self.result: typing.List[CriteriaEntropy.ResultType] = []
        self.cal_entropy_all()

    def cal_entropy(self, input: InputType, pick: typing.Tuple[int, ...]) -> float:
        picked_groups = [criteria[self.groups[i]] for i in pick]

        result_map: typing.Dict[typing.Tuple[int, ...], int] = {}

        for comb in self.combinations:
            picked_comb = [comb[i] for i in pick]
            cris = [picked_groups[i][picked_comb[i]]
                    for i in range(len(picked_groups))]

            result = tuple([cri(input) for cri in cris])

            result_map.setdefault(result, 0)
            result_map[result] = result_map[result] + 1

        ent = 0
        for v in result_map.values():
            p = v / len(self.combinations)
            ent = ent - p * math.log2(p)

        return ent

    def cal_entropy_all(self):
        codes = [v for v in product(range(1, 6), range(1, 6), range(1, 6))]

        picks = [x for x in combinations(range(len(self.groups)), 1)] + [x for x in combinations(
            range(len(self.groups)), 2)] + [x for x in combinations(range(len(self.groups)), 3)]

        self.result = []

        for pick in picks:
            for code in codes:
                ent = self.cal_entropy(code, pick)
                self.result.append(
                    (ent, [self.groups[i]+1 for i in pick], code))

        sum_each = {}
        for ent, pick, _ in self.result:
            if len(pick) == 1:
                old = sum_each.setdefault(pick[0], ent)
                sum_each[pick[0]] = old + ent

        for i in self.result:
            i[1].sort(key=lambda x: sum_each[x], reverse=True)

        self.result.sort(key=lambda x: sum_each[x[1][0]], reverse=True)
        self.result.sort(key=lambda x: len(x[1]))
        self.result.sort(key=lambda x: x[0], reverse=True)

    def print_best(self, n=3):
        print("Best entropy for each input:")
        for i in range(n):
            if i >= len(self.result):
                break
            print(
                f"\tEntropy: {self.result[i][0]}, Criteria: {self.result[i][1]}, Input: {self.result[i][2]}")

    def print_best_for(self, target: InputType, n=3):
        print("Best entropy for same input:")
        filtered = [i for i in self.result if i[2] == target and len(i[1]) < 3]

        sum_each = {}
        for ent, pick, _ in filtered:
            if len(pick) == 1:
                old = sum_each.setdefault(pick[0], ent)
                sum_each[pick[0]] = old + ent

        for i in self.result:
            i[1].sort(key=lambda x: sum_each[x], reverse=True)

        for i in range(n):
            if i >= len(filtered):
                break
            print(
                f"\tEntropy: {filtered[i][0]}, Criteria: {filtered[i][1]}, Input: {filtered[i][2]}")
