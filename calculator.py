import typing
from criteria import Criterion, InputType, criteria
from itertools import chain, product


def build_values() -> typing.List[InputType]:
    return product(range(1, 6), range(1, 6), range(1, 6))


def build_criteria_idxes(v: typing.List[Criterion]):
    return [range(i) for i in [len(i) for i in v]]


class GameState:
    def remove_impossible_codes(self):
        filtered = []
        for v in self.possible_codes:
            # for a specific criteria group, there must be at least one criterion that is satisfied
            goodv = True
            for idx in self.activated_group_idx:
                if not any(map(lambda cri: cri(v), criteria[idx])):
                    goodv = False
                    break
            if goodv:
                filtered.append(v)
        self.possible_codes = filtered

    def remove_impossible_criteria_combinations(self):
        for i in range(len(self.activated_group_idx)):
            filtered = []
            for cri_idx in self.possible_criteria_combination[i]:
                cri = criteria[self.activated_group_idx[i]][cri_idx]
                if any(map(lambda c: cri(c), self.possible_codes)):
                    filtered.append(cri_idx)
            self.possible_criteria_combination[i] = filtered

    def __init__(self, activated_groups: typing.List[int]):
        self.possible_codes = build_values()
        self.activated_group_idx = activated_groups
        self.possible_criteria_combination = [
            list(range(i)) for i in [len(criteria[i]) for i in self.activated_group_idx]]
        self.remove_impossible_codes()
        self.remove_impossible_criteria_combinations()

    def print(self):
        GREY = '\033[90m'
        WHITE = '\033[0m'

        print(WHITE + "Possible criteria combination:")
        for i in range(len(self.activated_group_idx)):
            group = criteria[self.activated_group_idx[i]]
            print(WHITE + "Group %d: \t" %
                  (self.activated_group_idx[i] + 1), end="")
            for j in range(len(group)):
                if not j == 0:
                    print(WHITE + " | ", end="")
                if j in self.possible_criteria_combination[i]:
                    print(WHITE + "%s" % (group[j]), end="")
                else:
                    print(GREY + "%s" % (group[j]), end="")
            print("")

        print(WHITE + "Possible values:")

        def print_color(l: typing.Set[int]):
            for i in range(1, 6):
                if not i == 1:
                    print(WHITE + " | ", end="")
                if i in l:
                    print(WHITE + "%d" % i, end="")
                else:
                    print(GREY + "%d" % i, end="")
            print("")

        print(WHITE + "Blue:\t", end="")
        print_color(set(map(lambda c: c[0], self.possible_codes)))

        print(WHITE + "Yellow:\t", end="")
        print_color(set(map(lambda c: c[1], self.possible_codes)))

        print(WHITE + "Purple:\t", end="")
        print_color(set(map(lambda c: c[2], self.possible_codes)))


if __name__ == "__main__":
    a = input("Input activated groups (separated by \",\"): ")
    groups = [int(i)-1 for i in a.split(',')]
    gs = GameState(groups)
    gs.print()
