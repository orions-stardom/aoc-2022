#!/usr/bin/env -S pdm run python
import more_itertools as mit
import string

def _parse(rawdata):
    return rawdata.splitlines()

def part_1(*rucksacks):
    r"""
    >>> part_1(*_parse('''\
    ... vJrwpWtwJgWrhcsFMMfFFhFp
    ... jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    ... PmmdzqPrVvPwwTWBwg
    ... wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ... ttgJtRGJQctTZtZT
    ... CrZsJsPPZsGzwwsLwLmpwMDw
    ... '''))
    157
    """
    def split(rucksack):
        size = len(rucksack)//2
        return rucksack[:size], rucksack[size:]
    def common(r1, r2):
        return mit.only(set(r1) & set(r2))
    return sum(string.ascii_letters.index(common(*r))+1 for r in map(split, rucksacks))


def part_2(*rucksacks):
    r"""
    >>> part_2(*_parse('''\
    ... vJrwpWtwJgWrhcsFMMfFFhFp
    ... jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    ... PmmdzqPrVvPwwTWBwg
    ... wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ... ttgJtRGJQctTZtZT
    ... CrZsJsPPZsGzwwsLwLmpwMDw
    ... '''))
    70
    """
    def common(r1, r2, r3):
        return mit.only(set(r1) & set(r2) & set(r3))

    return sum(string.ascii_letters.index(common(*g))+1 for g in mit.chunked(rucksacks, 3))

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
