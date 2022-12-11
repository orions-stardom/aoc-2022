#!/usr/bin/env -S pdm run python

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... mjqjpqmgbljsphdztnvjfqwrcgsmlb
    ... ''')
    7
    >>> part_1('''\
    ... bvwbjplbgvbhsrlpgdmjqwftvncz
    ... ''')
    5
    >>> part_1('''\
    ... nppdvjthqldpwncqszvftbrmjlhg
    ... ''')
    6
    >>> part_1('''\
    ... nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
    ... ''')
    10
    >>> part_1('''\
    ... zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
    ... ''')
    11
    """
    for i in range(4, len(rawdata)):
        if len(set(rawdata[i-4:i])) == 4:
            return i

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... mjqjpqmgbljsphdztnvjfqwrcgsmlb
    ... ''')
    19
    >>> part_2('''\
    ... bvwbjplbgvbhsrlpgdmjqwftvncz
    ... ''')
    23
    >>> part_2('''\
    ... nppdvjthqldpwncqszvftbrmjlhg
    ... ''')
    23
    >>> part_2('''\
    ... nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
    ... ''')
    29
    >>> part_2('''\
    ... zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
    ... ''')
    26
    """
    for i in range(14, len(rawdata)):
        if len(set(rawdata[i-14:i])) == 14:
            return i

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
