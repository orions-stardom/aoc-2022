#!/usr/bin/env -S pdm run python
from parse import parse

def ranges(rawdata):
    return [parse("{:d}-{:d},{:d}-{:d}", line) for line in rawdata.splitlines()]

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... 2-4,6-8
    ... 2-3,4-5
    ... 5-7,7-9
    ... 2-8,3-7
    ... 6-6,4-6
    ... 2-6,4-8
    ... ''')
    2
    """
    return sum((a>=c and b<=d) or (c>=a and d<=b) for a,b,c,d in ranges(rawdata))


def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... 2-4,6-8
    ... 2-3,4-5
    ... 5-7,7-9
    ... 2-8,3-7
    ... 6-6,4-6
    ... 2-6,4-8
    ... ''')
    4
    """
    return sum(bool(set(range(a,b+1))&set(range(c,d+1))) for a,b,c,d in ranges(rawdata))

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
        print(f"Solution to part {part}: ", solution, sep="\n")
        # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
        aocd.submit(solution, part='ab'[part-1], reopen=False)
