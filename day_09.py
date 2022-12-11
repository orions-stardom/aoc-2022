#!/usr/bin/env -S pdm run python
import more_itertools as mit

def moves(rawdata):
    return [(line.split()[0], int(line.split()[1])) for line in rawdata.splitlines()]

def follow(t, h):
    delta = h - t
    dx, dy = abs(delta.real), abs(delta.imag)
    if dx > 1 and dy <= 1:
        return complex((h.real+t.real)//2, h.imag)
    elif dx <= 1 and dy > 1:
        return complex(h.real, (h.imag+t.imag)//2)
    elif dx > 1 and dy > 1:
        return complex((h.real+t.real)//2,(h.imag+t.imag)//2)

    return t

directions = {
    "R": 1+0j,
    "L": -1+ 0j,
    "U": 0+1j,
    "D": 0+-1j
}

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... R 4
    ... U 4
    ... L 3
    ... D 1
    ... R 4
    ... D 1
    ... L 5
    ... R 2
    ... ''')
    13
    """
    h = 0+0j
    t = 0+0j
    visited = {t}

    for d,n in moves(rawdata):
        delta = directions[d]

        for _ in range(n):
            h += delta
            t = follow(t, h) 
            visited.add(t)
            
    return len(visited)


def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... R 4
    ... U 4
    ... L 3
    ... D 1
    ... R 4
    ... D 1
    ... L 5
    ... R 2
    ... ''')
    1

    >>> part_2('''\
    ... R 5
    ... U 8
    ... L 8
    ... D 3
    ... R 17
    ... D 10
    ... L 25
    ... U 20
    ... ''')
    36
    """
    knots = [0+0j] * 10
    visited = {knots[-1]}

    for d,n in moves(rawdata):
        delta = directions[d]

        for _ in range(n):
            knots[0] += delta
            for i,j in mit.pairwise(range(len(knots))):
                knots[j] = follow(knots[j], knots[i])
            
            visited.add(knots[-1])
    
    return len(visited)

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
