#!/usr/bin/env -S pdm run python
import more_itertools as mit
import parse

def cave_map(rawdata:str) -> set[complex]:
    result = set()

    @parse.with_pattern(r"\d+,\d+")
    def cave_point(string:str) -> complex:
        x, y = string.split(",")
        return complex(int(x), int(y))

    for line in rawdata.splitlines():
        rock_segments = parse.findall("{:cave_point}", line, extra_types=dict(cave_point=cave_point))
        for a,b in mit.pairwise(r[0] for r in rock_segments):
            if a.real == b.real:
                x = int(a.real)
                start, end = min(a.imag,b.imag), max(a.imag,b.imag)
                for y in range(int(start), int(end)+1):
                    result.add(complex(x,y))
            elif a.imag == b.imag:
                y = int(a.imag)
                start, end = min(a.real,b.real), max(a.real,b.real)
                for x in range(int(start), int(end)+1):
                    result.add(complex(x,y))
            else:
                raise ValueError(a,b)

    return result

def part_1(rawdata:str):
    r"""
    >>> part_1('''\
    ... 498,4 -> 498,6 -> 496,6
    ... 503,4 -> 502,4 -> 502,9 -> 494,9
    ... ''')
    24
    """
    rocks, sand = cave_map(rawdata), set()
    # +y axis points down so bottom point must be at the highest y
    bottom = max(z.imag for z in rocks)

    z = 500+0j
    while z.imag <= bottom:
        for dz in 1j, -1+1j, 1+1j:
            if z+dz not in rocks|sand:
                z += dz
                break
        else:
            # if all directions are blocked we stop here
            sand.add(z)
            z = 500+0j
            
    return len(sand)

def part_2(rawdata:str):
    r"""
    >>> part_2('''\
    ... 498,4 -> 498,6 -> 496,6
    ... 503,4 -> 502,4 -> 502,9 -> 494,9
    ... ''')
    93
    """
    rocks, sand = cave_map(rawdata), set()
    # +y axis points down so bottom point is highest y
    floor_level = max(z.imag for z in rocks) + 2

    z = 500+0j
    while 500+0j not in sand:
        for dz in 1j, -1+1j, 1+1j:
            cand = z+dz
            # resist the temptation to union them like part 1..
            # because that makes the whole thing quadratic
            if cand not in rocks and cand not in sand:
                # keep falling
                z = cand
                break
        else:
            # all directions are blocked so we stop here
            sand.add(z)
            z = 500+0j

        if z.imag + 1 == floor_level:
            # can't fall much further than the bottom
            sand.add(z)
            z = 500+0j

    return len(sand)

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
