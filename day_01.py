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
    import argparse
    import aocd
    import doctest
    import sys
     
    cli = argparse.ArgumentParser()
    all_parts = []
    try:
        all_parts.append(part_1) 
    except NameError:
        pass

    try:
        all_parts.append(part_2)
    except NameError:
        pass

    cli.add_argument("--part", action="append", choices=all_parts, default=all_parts, dest="do_parts")
    cli.add_argument("--all-parts", action="store_const", const=all_parts, dest="do_parts")
    cli.add_argument("--skip-tests", action="store_true")
    cli.add_argument("--no-submit", action="store_false", dest="submit")

    args = cli.parse_args()

    if not args.skip_tests:
        failure, tests = doctest.testmod()
        if failure > 0:
            sys.exit(f"Failed {failure}/{tests} tests")
   
    # aocd has some magic introspection but it doesnt like my naming conventions
    from pathlib import Path
    f = Path(__file__)
    puzzle_input = aocd.get_data(
        year=f.parent.name.removeprefix("aoc-"),
        day=int(f.stem.removeprefix("day_")))
    
    for part in args.do_parts: 
        solution = part(*_parse(puzzle_input))
        part_number = int(part.__name__.removeprefix("part_"))
        print(f"Solution to part {part_number}: ", solution, sep="\n")
        if args.submit:
            # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
            aocd.submit(solution, part='ab'[part_number-1], reopen=False)

