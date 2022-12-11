#!/usr/bin/env -S pdm run python
import parse
import heapq
import math
from dataclasses import dataclass
from typing import NamedTuple, Callable

@dataclass
class Monkey:
    """
    >>> m = Monkey.parse('''\
    ... Monkey 0:
    ...   Starting items: 79, 98
    ...   Operation: new = old * 19
    ...   Test: divisible by 23
    ...     If true: throw to monkey 2
    ...     If false: throw to monkey 3
    ... ''')
    >>> m.items
    [79, 98]
    >>> m.operation(1)
    19
    >>> m.divisor
    23
    >>> m.true_target
    2
    >>> m.false_target
    3

    """
    items: list[int]
    operation: Callable[int,int]
    divisor: int
    true_target: int
    false_target: int
    items_touched: int = 0

    @classmethod
    def parse(cls, data):
        lines = data.splitlines()[1:]
        return cls(
            [r[0] for r in parse.findall("{:d}", lines[0])],
            eval(lines[1].replace("Operation: new =", "lambda old:")),
            parse.search("{:d}", lines[2])[0],
            parse.search("{:d}", lines[3])[0],
            parse.search("{:d}", lines[4])[0],
        )


def run_sim(rawdata:str, *, nrounds:int, relief_ratio:int):
    monkeys = [Monkey.parse(data) for data in rawdata.split("\n\n")]
    lcm = math.prod(m.divisor for m in monkeys) # all the divisors turn out to be prime

    for _ in range(nrounds):
        for monkey in monkeys:
            for item in monkey.items:
                new_worry_level = (monkey.operation(item) // relief_ratio) % lcm
                target = monkey.true_target if new_worry_level % monkey.divisor == 0 else monkey.false_target
                monkeys[target].items.append(new_worry_level)
                monkey.items_touched += 1

            monkey.items.clear()

    m1, m2 = heapq.nlargest(2, monkeys, key=lambda m: m.items_touched)
    return m1.items_touched * m2.items_touched


def part_1(data:str):
    """
    >>> part_1('''\
    ... Monkey 0:
    ...   Starting items: 79, 98
    ...   Operation: new = old * 19
    ...   Test: divisible by 23
    ...     If true: throw to monkey 2
    ...     If false: throw to monkey 3
    ... 
    ... Monkey 1:
    ...   Starting items: 54, 65, 75, 74
    ...   Operation: new = old + 6
    ...   Test: divisible by 19
    ...     If true: throw to monkey 2
    ...     If false: throw to monkey 0
    ... 
    ... Monkey 2:
    ...   Starting items: 79, 60, 97
    ...   Operation: new = old * old
    ...   Test: divisible by 13
    ...     If true: throw to monkey 1
    ...     If false: throw to monkey 3
    ... 
    ... Monkey 3:
    ...   Starting items: 74
    ...   Operation: new = old + 3
    ...   Test: divisible by 17
    ...     If true: throw to monkey 0
    ...     If false: throw to monkey 1
    ... ''')
    10605
    """
    return run_sim(data, nrounds=20, relief_ratio=3)


def part_2(data:str):
    """
    >>> part_2('''\
    ... Monkey 0:
    ...   Starting items: 79, 98
    ...   Operation: new = old * 19
    ...   Test: divisible by 23
    ...     If true: throw to monkey 2
    ...     If false: throw to monkey 3
    ... 
    ... Monkey 1:
    ...   Starting items: 54, 65, 75, 74
    ...   Operation: new = old + 6
    ...   Test: divisible by 19
    ...     If true: throw to monkey 2
    ...     If false: throw to monkey 0
    ... 
    ... Monkey 2:
    ...   Starting items: 79, 60, 97
    ...   Operation: new = old * old
    ...   Test: divisible by 13
    ...     If true: throw to monkey 1
    ...     If false: throw to monkey 3
    ... 
    ... Monkey 3:
    ...   Starting items: 74
    ...   Operation: new = old + 3
    ...   Test: divisible by 17
    ...     If true: throw to monkey 0
    ...     If false: throw to monkey 1
    ... ''')
    2713310158
    """ 
    return run_sim(data, nrounds=10_000, relief_ratio=1)

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
