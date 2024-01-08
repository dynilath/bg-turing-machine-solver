import typing
from criteria import Criterion, InputType, criteria
from itertools import chain, product
from entropy import CriteriaEntropy


def build_values() -> typing.List[InputType]:
    return [v for v in product(range(1, 6), range(1, 6), range(1, 6))]


class GameState:
    def remove_impossible_codes(self):
        filtered = []
        for v in self.possible_codes:
            # for a valid code, there must be at least one criteria combination that is satisfied
            goodv = False
            for comb in self.possible_criteria_combination:
                result = [self.activated_groups[i][comb[i]]
                          (v) for i in range(len(comb))]
                if all(result):
                    goodv = True
                    break
            if goodv:
                filtered.append(v)
        self.possible_codes = filtered

    def remove_multisolve_combinations(self):
        filtered = []
        # for a valid combination, one and only one code may satisfy it
        for comb in self.possible_criteria_combination:
            cris = [self.activated_groups[i][comb[i]]
                    for i in range(len(comb))]
            goodcomb = 0
            for code in product(range(1, 6), range(1, 6), range(1, 6)):
                result = [cri(code) for cri in cris]
                if all(result):
                    goodcomb += 1
            if goodcomb == 1:
                filtered.append(comb)

        self.possible_criteria_combination = filtered

    def print_possibles(self):
        for i in self.possible_criteria_combination:
            for code in product(range(1, 6), range(1, 6), range(1, 6)):
                result = [self.activated_groups[j][i[j]](code)
                          for j in range(len(i))]
                if all(result):
                    print(f"Code {code} satisfies {i}")

    def remove_no_solve_combinations(self):
        filtered = []
        for comb in self.possible_criteria_combination:
            for code in product(range(1, 6), range(1, 6), range(1, 6)):
                result = [self.activated_groups[j][comb[j]](code)
                          for j in range(len(comb))]
                if all(result):
                    filtered.append(comb)

        self.possible_criteria_combination = filtered

    def remove_locked_combinations(self):
        # as combination index, -1 for concerned index
        KeyType = typing.Tuple[int, ...]
        ValueType = typing.Set[int]

        filterSet = set()
        # for a given part on criteria, no other criteria part is locked
        xfiltermap: typing.Dict[KeyType, ValueType] = {}
        for comb in self.possible_criteria_combination:
            for i in range(len(comb)):
                cp_comb = tuple(
                    [comb[j] if j != i else -1 for j in range(len(comb))])
                xfiltermap.setdefault(cp_comb, set())
                xfiltermap[cp_comb].add(comb[i])
        for k, v in xfiltermap.items():
            if len(v) == 1:
                filterSet.add(k)

        for f in filterSet:
            print(f"Combination {f} is locked")

        filtered = []
        for comb in self.possible_criteria_combination:
            goodcomb = True
            for i in range(len(comb)):
                cp_comb = tuple(
                    [comb[j] if j != i else -1 for j in range(len(comb))])
                if cp_comb in filterSet:
                    goodcomb = False
                    break
            if goodcomb:
                filtered.append(comb)

        self.possible_criteria_combination = filtered

    def remove_impossible_criteria_combinations(self):
        filtered = []
        for comb in self.possible_criteria_combination:
            # for a valid combination, there must be at least one code that is satisfied
            goodcomb = False
            for v in self.possible_codes:
                result = [self.activated_groups[i][comb[i]]
                          (v) for i in range(len(comb))]
                if all(result):
                    goodcomb = True
                    break
            if goodcomb:
                filtered.append(comb)

        self.possible_criteria_combination = filtered

    def purge(self):
        while True:
            old_len1 = len(self.possible_codes)
            old_len2 = len(self.possible_criteria_combination)
            self.remove_impossible_codes()
            self.remove_impossible_criteria_combinations()
            if old_len1 == len(self.possible_codes) and old_len2 == len(self.possible_criteria_combination):
                break

    def __init__(self, activated_groups: typing.List[int]):
        self.possible_codes = build_values()
        self.activated_group_idx = activated_groups
        self.activated_groups = [criteria[i] for i in self.activated_group_idx]
        self.possible_criteria_combination: typing.List[typing.Tuple[int, ...]] = [
            i for i in product(*[
                list(range(i)) for i in [len(criteria[i]) for i in self.activated_group_idx]])]
        # Stage 1: remove impossible criteria combinations
        self.remove_no_solve_combinations()
        # Stage 2: remove criteria combinations that have redundant
        self.remove_locked_combinations()
        # print("Stage 2:")
        # self.print_possibles()
        # Stage 3: remove criteria combinations that have multiple solutions
        self.remove_multisolve_combinations()

        print("Stage Finished:")
        self.purge()
        self.print_possibles()

    def print(self):
        GREY = '\033[90m'
        WHITE = '\033[0m'
        GREEN = '\033[92m'

        cris_flags = [[False for i in range(
            len(self.activated_groups[j]))] for j in range(len(self.activated_groups))]
        for comb in self.possible_criteria_combination:
            for j in range(len(comb)):
                cris_flags[j][comb[j]] = True

        print(WHITE + "Possible criteria combination:")
        for i in range(len(self.activated_group_idx)):
            group = criteria[self.activated_group_idx[i]]
            print(WHITE + "\tGroup %d: \t" %
                  (self.activated_group_idx[i] + 1), end="")
            group_flags = cris_flags[i]

            for j in range(len(group)):
                if not j == 0:
                    print(WHITE + " | ", end="")
                if group_flags[j]:
                    print(GREEN + "%s" % (group[j]), end="")
                else:
                    print(GREY + "%s" % (group[j]), end="")
            print("")

        print(WHITE + "Possible values:")

        def print_color(l: typing.Set[int]):
            for i in range(1, 6):
                if not i == 1:
                    print(WHITE + " | ", end="")
                if i in l:
                    print(GREEN + "%d" % i, end="")
                else:
                    print(GREY + "%d" % i, end="")
            print("")

        print(WHITE + "\tBlue:\t", end="")
        print_color(set(map(lambda c: c[0], self.possible_codes)))

        print(WHITE + "\tYellow:\t", end="")
        print_color(set(map(lambda c: c[1], self.possible_codes)))

        print(WHITE + "\tPurple:\t", end="")
        print_color(set(map(lambda c: c[2], self.possible_codes)))

        print(WHITE, end="")

    def put_result(self, input: InputType, which: int, result: bool):
        target = self.activated_group_idx.index(which)
        group = criteria[which]
        filtered = []
        for comb in self.possible_criteria_combination:
            if group[comb[target]](input) == result:
                filtered.append(comb)
        self.possible_criteria_combination = filtered
        self.purge()


class History:
    HistoryItem = typing.Tuple[InputType,
                               typing.List[typing.Union[bool, None]]]

    def __init__(self, activated_groups: typing.List[int]):
        self.history: typing.List[History.HistoryItem] = []
        self.groups = activated_groups

    def put_result(self, code: InputType, which: int, result: bool):
        idx = self.groups.index(which)
        if len(self.history) == 0 or self.history[-1][0] != code:
            self.history.append(
                (code, [None for _ in range(len(self.groups))]))
        self.history[-1][1][idx] = result

    def print(self):
        print("History:")
        for i in self.history:
            print(f"\tCode: {i[0]}\t", end="")
            for j in range(len(self.groups)):
                if i[1][j] is None:
                    print("| _ ", end="")
                elif i[1][j]:
                    print("| \033[92mO\033[0m ", end="")
                else:
                    print("| \033[91mX\033[0m ", end="")
            print("|")


if __name__ == "__main__":
    a = input("Input activated criteria (separated by \",\"): ")
    groups = [int(i)-1 for i in a.split(',')]

    if len(groups) == 0 or not all([i in range(0, len(criteria)) for i in groups]):
        raise ValueError("Invalid criteria!")

    gs = GameState(groups)
    gs.print()
    en = CriteriaEntropy(gs.activated_group_idx,
                         gs.possible_criteria_combination)
    en.print_best()

    hs = History(groups)

    round_num = 1
    while True:
        print("\n\033[94m>> Round %d\033[0m" % round_num)
        a = input(
            "Input code, criteria and result (separated by \",\", use O/X for result): ")
        if a == 'exit':
            break

        try:
            code1, code2, code3, whi, result = a.split(',')
            code = (int(code1), int(code2), int(code3))
            if all([i in range(1, 6) for i in code]) == False:
                raise ValueError("Invalid code!")

            which = int(whi) - 1
            if which not in groups:
                raise ValueError("Invalid criteria!")

            result = result.lower()
            if result == 'o':
                result = True
            elif result == 'x':
                result = False
            else:
                raise ValueError("Invalid result!")
        except ValueError as e:
            print(f"\033[91mInvalid input:{e}\033[0m")
            continue

        hs.put_result(code, which, result)
        hs.print()

        gs.put_result(code, which, result)
        gs.print()

        en = CriteriaEntropy(gs.activated_group_idx,
                             gs.possible_criteria_combination)
        en.print_best()
        en.print_best_for(code)
        round_num += 1
