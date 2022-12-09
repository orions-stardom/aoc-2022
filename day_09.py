#!/usr/bin/env -S pdm run python
from typing import NamedTuple
import math
import more_itertools as mit

def _parse(rawdata):
    return [(line.split()[0], int(line.split()[1])) for line in rawdata.splitlines()]

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, d):
        dx, dy = d
        return Point(self.x+dx, self.y+dy)

    def __sub__(self, p):
        return (self.x - p.x, self.y - p.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def follow(self, h):
        dx, dy = abs(h.x-self.x), abs(h.y-self.y)
        if dx > 1 and dy <= 1:
            return Point((h.x+self.x)//2, h.y)
        elif dx <= 1 and dy > 1:
            return Point(h.x, (h.y+self.y)//2)
        elif dx > 1 and dy > 1:
            return Point((h.x+self.x)//2,(h.y+self.y)//2)

        return self


directions = {
    "R": (1,0),
    "L": (-1, 0),
    "U": (0,1),
    "D": (0,-1)
}


def part_1(*lines):
    r"""
    >>> part_1(*_parse('''\
    ... R 4
    ... U 4
    ... L 3
    ... D 1
    ... R 4
    ... D 1
    ... L 5
    ... R 2
    ... '''))
    13
    """
    h = Point(0,0)
    t = Point(0,0)
    visited = {t}

    for d,n in lines:
        delta = directions[d]

        for _ in range(n):
            h += delta
            t = t.follow(h) 
            visited.add(t)
            
    return len(visited)


def part_2(*lines):
    r"""
    >>> part_2(*_parse('''\
    ... R 4
    ... U 4
    ... L 3
    ... D 1
    ... R 4
    ... D 1
    ... L 5
    ... R 2
    ... '''))
    1

    >>> part_2(*_parse('''\
    ... R 5
    ... U 8
    ... L 8
    ... D 3
    ... R 17
    ... D 10
    ... L 25
    ... U 20
    ... '''))
    36
    """
    knots = [Point(0,0) for _ in range(10)]
    visited = {knots[-1]}

    for d,n in lines:
        delta = directions[d]

        for _ in range(n):
            knots[0] += delta
            for i,j in mit.pairwise(range(len(knots))):
                knots[j] = knots[j].follow(knots[i])
                # dx, dy = abs(knots[i].x-knots[j].x), abs(knots[i].y-knots[j].y)
                # if dx > 1:
                #     knots[j] = Point((knots[i].x+knots[j].x)//2, knots[i].y)
                # elif dy > 1:
                #     knots[j] = Point(knots[i].x, (knots[i].y+knots[j].y)//2)
            
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

        solution = impl(*_parse(puzzle_input))
        print(f"Solution to part {part}: ", solution, sep="\n")
        # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
        aocd.submit(solution, part='ab'[part-1], reopen=False)
