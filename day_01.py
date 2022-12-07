#!/usr/bin/env -S pdm run python
import heapq
  
def _parse(rawdata):
    return [[int(x) for x in group.splitlines()] for group in rawdata.split("\n\n")]

def part_1(*elves):
    r"""
    >>> part_1(*_parse('''\
    ... 1000
    ... 2000
    ... 3000
    ...
    ... 4000
    ...
    ... 5000
    ... 6000
    ...
    ... 7000
    ... 8000
    ... 9000
    ...
    ... 10000
    ... '''))
    24000
    """
    return max(sum(e) for e in elves)

def part_2(*elves):
    r"""
    >>> part_2(*_parse('''\
    ... 1000
    ... 2000
    ... 3000
    ...
    ... 4000
    ...
    ... 5000
    ... 6000
    ...
    ... 7000
    ... 8000
    ... 9000
    ...
    ... 10000
    ... '''))
    45000
    """
    return sum(heapq.nlargest(3, (sum(e) for e in elves)))

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

        solution = impl(*_parse(puzzle_input))
        print(f"Solution to part {part}: ", solution, sep="\n")
        # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
        aocd.submit(solution, part='ab'[part-1], reopen=False)

