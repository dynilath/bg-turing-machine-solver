import typing
import math
from itertools import combinations, product

from criteria import InputType, criteria


class CriteriaEntropy:
    def __init__(self, actived_group: typing.List[int], possible_combination: typing.List[typing.List[int]]):
        self.groups = actived_group
        self.combinations = possible_combination

    def cal_entropy(self, input: InputType, pick: typing.Tuple[int, ...]) -> float:
        picked_groups = [criteria[self.groups[i]] for i in pick]
        picked_combines = [self.combinations[i] for i in pick]

        def cal_result(t_comb: typing.List[int]):
            cris = [picked_groups[i][t_comb[i]]
                    for i in range(len(picked_groups))]
            return tuple([x(input) for x in cris])

        result_map: typing.Dict[typing.Tuple[int, ...], int] = {}

        for comb in product(*picked_combines):
            result = cal_result(comb)
            result_map.setdefault(result, 0)
            result_map[result] = result_map[result] + 1

        ent = 0
        for v in result_map.values():
            p = v / len(result_map)
            ent = ent - p * math.log2(p)

        return ent

    def cal_entropy_all(self):
        values = [v for v in product(range(1, 6), range(1, 6), range(1, 6))]

        picks = [x for x in combinations(range(len(self.groups)), 1)] + [x for x in combinations(
            range(len(self.groups)), 2)] + [x for x in combinations(range(len(self.groups)), 3)]

        result: typing.List[typing.Tuple[float,
                                         typing.List[int], typing.Tuple[int, int, int]]] = []

        for pick in picks:
            for value in values:
                ent = self.cal_entropy(value, pick)
                result.append(
                    (ent, [self.groups[i]+1 for i in pick], value))

        result.sort(key=lambda x: x[0] + len(x[1])*100, reverse=True)
        return result

    def cal_entropy_for_input(self, value: InputType):
        picks = [x for x in combinations(range(len(self.groups)), 1)] + [x for x in combinations(
            range(len(self.groups)), 2)] + [x for x in combinations(range(len(self.groups)), 3)]

        result: typing.List[typing.Tuple[float,
                                         typing.List[int], typing.Tuple[int, int, int]]] = []
        for pick in picks:
            ent = self.cal_entropy(value, pick)
            result.append((ent, [self.groups[i]+1 for i in pick], value))

        result.sort(key=lambda x: x[0] + len(x[1])*100, reverse=True)
        return result
