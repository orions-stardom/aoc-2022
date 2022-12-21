#!/usr/bin/env -S pdm run python

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... root: pppw + sjmn
    ... dbpl: 5
    ... cczh: sllz + lgvd
    ... zczc: 2
    ... ptdq: humn - dvpt
    ... dvpt: 3
    ... lfqf: 4
    ... humn: 5
    ... ljgn: 2
    ... sjmn: drzm * dbpl
    ... sllz: 4
    ... pppw: cczh / lfqf
    ... lgvd: ljgn * ptdq
    ... drzm: hmdt - zczc
    ... hmdt: 32
    ... ''')
    152
    """
    monkeys = dict(line.split(":") for line in rawdata.splitlines())
    def solve(monkey:str) -> int:
        match monkeys[monkey].split():
            case str() as n1, "+", str() as n2:
                return solve(n1) + solve(n2)
            case str() as n1, "-", str() as n2:
                return solve(n1) - solve(n2)
            case str() as  n1, "*", str() as n2:
                return solve(n1) * solve(n2)
            case str() as  n1, "/", str() as n2:
                return solve(n1) // solve(n2)
            case [str() as n]:
                return int(n)

    return solve("root")

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... root: pppw + sjmn
    ... dbpl: 5
    ... cczh: sllz + lgvd
    ... zczc: 2
    ... ptdq: humn - dvpt
    ... dvpt: 3
    ... lfqf: 4
    ... humn: 5
    ... ljgn: 2
    ... sjmn: drzm * dbpl
    ... sllz: 4
    ... pppw: cczh / lfqf
    ... lgvd: ljgn * ptdq
    ... drzm: hmdt - zczc
    ... hmdt: 32
    ... ''')
    301
    """
    monkeys = dict(line.split(":") for line in rawdata.splitlines())

    class Placeholder(int):
        def __init__(self):
            self.ops = []

        def __add__(self, other):
            self.ops.append(lambda n: n-other)
            return self

        __radd__ = __add__

        def __sub__(self, other):
            self.ops.append(lambda n: n+other)
            return self

        def __rsub__(self, other):
            self.ops.append(lambda n: other - n)
            return self

        def __mul__(self, other):
            self.ops.append(lambda n: n // other)
            return self

        __rmul__ = __mul__

        def __floordiv__(self, other):
            self.ops.append(lambda n: n*other)
            return self

        def __rfloordiv__(self, other):
            self.ops.append(lambda n: other // n)
            return self

        def __eq__(self, other):
            for op in reversed(self.ops):
                other = op(other)
            return other

        def __repr__(self):
            return "placeholder"

    def solve(monkey:str) -> int:
        if monkey == "humn":
            return Placeholder()

        job = monkeys[monkey].split()
        if monkey == "root":
            n1, _, n2 = job
            return solve(n1) == solve(n2)

        match job:
            case str() as n1, "+", str() as n2:
                return solve(n1) + solve(n2) 
            case str() as n1, "-", str() as n2:
                return solve(n1) - solve(n2)
            case str() as  n1, "*", str() as n2:
                return solve(n1) * solve(n2)
            case str() as  n1, "/", str() as n2:
                return solve(n1) // solve(n2)
            case [str() as n]:
                return int(n)

    return solve("root")

if __name__ == "__main__":
    import aocd
    import doctest
    import sys
     
    failure, tests = doctest.testmod()
    if failure > 0:
        sys.exit(f"Failed {failure}/{tests} tests")
   
    # aocd has some magic introspection but it doesnt like my naming conventions
    from pathlib import Path
    f = Path(__file__)
    puzzle_input = aocd.get_data(
        year=f.parent.name.removeprefix("aoc-"),
        day=int(f.stem.removeprefix("day_")))
    
    for part in 1, 2:
        try:
            impl = globals()[f"part_{part}"]
        except KeyError:
            print(f"No part {part} - skipping")
            continue

        solution = impl(puzzle_input)
        if solution is not None:
            print(f"Solution to part {part}: ", solution, sep="\n")
            # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
            aocd.submit(solution, part='ab'[part-1], reopen=False)
        else:
            print("No solution to part {part} {might need to be entered manually?)")
