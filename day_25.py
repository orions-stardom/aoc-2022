#!/usr/bin/env -S pdm run python

def snafu2int(snafu:str) -> int:
    """
    >>> snafu2int("1=-0-2")
    1747
    >>> snafu2int("20012")
    1257
    >>> snafu2int("1121-1110-1=0")
    314159265
    """
    n = 0
    for digit in snafu:
        n *= 5
        match digit:
            case "-":
                n -= 1
            case "=":
                n -= 2
            case d:
                n += int(d)
    return n

def int2snafu(n:int) -> str:
    """
    >>> print(int2snafu(314159265))
    1121-1110-1=0
    """
    digits = []
    carry = False
    while n or carry:
        n, mod = divmod(n+carry, 5)
        match mod:
            case 4:
                carry = True
                digits.append("-")
            case 3:
                carry = True
                digits.append("=")
            case _:
                carry = False
                digits.append(str(mod))

    return "".join(reversed(digits))

def part_1(rawdata):
    r"""
    >>> print(part_1('''\
    ... 1=-0-2
    ... 12111
    ... 2=0=
    ... 21
    ... 2=01
    ... 111
    ... 20012
    ... 112
    ... 1=-1=
    ... 1-12
    ... 12
    ... 1=
    ... 122
    ... '''))
    2=-1=0
    """
    return int2snafu(sum(snafu2int(line) for line in rawdata.splitlines()))


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
