#!/usr/bin/env -S pdm run python
def _parse(rawdata):
    return [line.split() for line in rawdata.splitlines()]


def part_1(*lines):
    r"""
    >>> part_1(*_parse('''\
    ... A Y
    ... B X
    ... C Z
    ... '''))
    15
    """
    score = 0
    for line in lines:
        opponent =  "ABC".index(line[0])
        you = "XYZ".index(line[1])

        # we have plays is 0-2 but need to inc score by 1-3
        score += you + 1
        if you == opponent:
            # draw
            score += 3

        needed = (opponent + 1) % 3
        if you == needed:
            score += 6

    return score

def part_2(*lines):
    r"""
    >>> part_2(*_parse('''\
    ... A Y
    ... B X
    ... C Z
    ... '''))
    12
    """
    score = 0
    for line in lines:
        opponent = "ABC".index(line[0])
        result = line[1]

        if result == "X":
            score += (opponent - 1) % 3 + 1
        elif result == "Y":
            score += (opponent + 1) + 3
        elif result == "Z":
            you = (opponent + 1) % 3
            score += (you + 1) + 6

    return score


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
