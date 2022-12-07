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
