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
        except NameError:
            print(f"No part {part} - skipping")
            continue

        solution = impl(*_parse(puzzle_input))
        print(f"Solution to part {part}: ", solution, sep="\n")
        # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
        aocd.submit(solution, part='ab'[part-1], reopen=False)
