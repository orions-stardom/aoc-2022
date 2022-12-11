#!/usr/bin/env -S pdm run python
import parse
import heapq
import math


class Monkey:
    """
    >>> m = Monkey('''\
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
    def __init__(self, description:str):
        lines = description.splitlines()[1:]
        self.items = [r[0] for r in parse.findall("{:d}", lines[0])]
        self.operation = eval(lines[1].replace("Operation: new =", "lambda old:"))
        self.divisor = parse.search("{:d}", lines[2])[0]
        self.true_target = parse.search("{:d}", lines[3])[0] 
        self.false_target = parse.search("{:d}", lines[4])[0] 
        self.items_touched = 0

    def inspect(self, relief_ratio:int):
        for item in self.items:
            new_worry_level = (self.operation(item) // relief_ratio)  % math.prod(m.divisor for m in monkies)
            target = self.true_target if new_worry_level % self.divisor == 0 else self.false_target
            monkies[target].items.append(new_worry_level)
            self.items_touched += 1
            
        self.items.clear()

def run(nrounds=20, *, relief_ratio:int):
    for _ in range(nrounds):
        for monkey in monkies:
            monkey.inspect(relief_ratio)

monkies = []
def parse_monkies(data:str):
    global monkies
    monkies = []

    for description in data.split("\n\n"):
        # assume they're in order.. 
        monkies.append(Monkey(description))

def part_1():
    """
    >>> parse_monkies('''\
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
    >>> part_1()
    10605
    """
    run(relief_ratio=3)

    m1, m2 = heapq.nlargest(2, monkies, key=lambda m: m.items_touched)
    return m1.items_touched * m2.items_touched


def part_2():
    """
    >>> parse_monkies('''\
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
    >>> part_2()
    2713310158
    """ 
    run(nrounds=10_000, relief_ratio=1)

    m1, m2 = heapq.nlargest(2, monkies, key=lambda m: m.items_touched)
    return m1.items_touched * m2.items_touched

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
        parse_monkies(puzzle_input)
        try:
            impl = globals()[f"part_{part}"]
        except KeyError:
            print(f"No part {part} - skipping")
            continue
        solution = impl()
        if solution is not None:
            print(f"Solution to part {part}: ", solution, sep="\n")
            # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
            aocd.submit(solution, part='ab'[part-1], reopen=False)
        else:
            print("No solution to part {part} {might need to be entered manually?)")
