#!/usr/bin/env -S pdm run python
from parse import parse

def _parse(rawdata):
    stack_data, instructions_data = rawdata.split("\n\n")
    instructions = [parse("move {:d} from {:d} to {:d}", line) for line in instructions_data.splitlines()]

    stack_lines = stack_data.splitlines()
    stacks = [[] for _ in stack_lines[-1].split()]
  
    stack_lines.pop(-1)
    stack_lines.reverse()

    for line in stack_lines:
        for i, crate in enumerate(line[1::4]):
            if not crate.isspace():
                stacks[i].append(crate)

    stacks.insert(0, []) # all the instructions are 1 based :(
    return stacks, instructions

def part_1(stacks, instructions):
    r"""
    >>> part_1(*_parse('''\
    ...     [D]    
    ... [N] [C]    
    ... [Z] [M] [P]
    ...  1   2   3 
    ... 
    ... move 1 from 2 to 1
    ... move 3 from 1 to 3
    ... move 2 from 2 to 1
    ... move 1 from 1 to 2
    ... '''))
    'CMZ'
    """
    # theres probably a clever faster way but fuck it
    for n, src, dest in instructions:
        stacks[dest].extend(reversed(stacks[src][-n::]))
        del stacks[src][-n:]

    return "".join(s[-1] for s in stacks[1:])


def part_2(stacks, instructions):
    r"""
    >>> part_2(*_parse('''\
    ...     [D]    
    ... [N] [C]    
    ... [Z] [M] [P]
    ...  1   2   3 
    ... 
    ... move 1 from 2 to 1
    ... move 3 from 1 to 3
    ... move 2 from 2 to 1
    ... move 1 from 1 to 2
    ... '''))
    'MCD'
    """
    # theres probably a clever faster way but fuck it
    for n, src, dest in instructions:
        stacks[dest].extend(stacks[src][-n:])
        del stacks[src][-n:]

    return "".join(s[-1] for s in stacks[1:])


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
