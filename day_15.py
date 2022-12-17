#!/usr/bin/env -S pdm run python
from parse import parse
import itertools as it

def parse_line(line:str) -> tuple[complex,complex]:
    r'''\
    >>> parse_line("Sensor at x=2, y=18: closest beacon is at x=-2, y=15")
    ((2+18j), (-2+15j))
    '''
    sx, sy, bx, by = parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", line)
    return (complex(sx,sy), complex(bx,by))

def part_1(rawdata:str, row:int=2000000):
    r"""
    >>> part_1('''\
    ... Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    ... Sensor at x=9, y=16: closest beacon is at x=10, y=16
    ... Sensor at x=13, y=2: closest beacon is at x=15, y=3
    ... Sensor at x=12, y=14: closest beacon is at x=10, y=16
    ... Sensor at x=10, y=20: closest beacon is at x=10, y=16
    ... Sensor at x=14, y=17: closest beacon is at x=10, y=16
    ... Sensor at x=8, y=7: closest beacon is at x=2, y=10
    ... Sensor at x=2, y=0: closest beacon is at x=2, y=10
    ... Sensor at x=0, y=11: closest beacon is at x=2, y=10
    ... Sensor at x=20, y=14: closest beacon is at x=25, y=17
    ... Sensor at x=17, y=20: closest beacon is at x=21, y=22
    ... Sensor at x=16, y=7: closest beacon is at x=15, y=3
    ... Sensor at x=14, y=3: closest beacon is at x=15, y=3
    ... Sensor at x=20, y=1: closest beacon is at x=15, y=3
    ... ''', 10)
    26
    """
    impossible = set()
    for sensor, beacon in map(parse_line, rawdata.splitlines()):
        delta = beacon - sensor 
        manhatten_dist = int(abs(delta.real)+abs(delta.imag))
      
        target_dy = abs(sensor.imag - row)
        dx = manhatten_dist - target_dy

        for x in range(int(sensor.real-dx), int(sensor.real+dx) + 1):
            z = complex(x,row)
            if z != beacon:
                impossible.add(z)

    return len(impossible)
            

def part_2(rawdata:str, max_coord:int=4000000):
    r"""
    >>> part_2('''\
    ... Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    ... Sensor at x=9, y=16: closest beacon is at x=10, y=16
    ... Sensor at x=13, y=2: closest beacon is at x=15, y=3
    ... Sensor at x=12, y=14: closest beacon is at x=10, y=16
    ... Sensor at x=10, y=20: closest beacon is at x=10, y=16
    ... Sensor at x=14, y=17: closest beacon is at x=10, y=16
    ... Sensor at x=8, y=7: closest beacon is at x=2, y=10
    ... Sensor at x=2, y=0: closest beacon is at x=2, y=10
    ... Sensor at x=0, y=11: closest beacon is at x=2, y=10
    ... Sensor at x=20, y=14: closest beacon is at x=25, y=17
    ... Sensor at x=17, y=20: closest beacon is at x=21, y=22
    ... Sensor at x=16, y=7: closest beacon is at x=15, y=3
    ... Sensor at x=14, y=3: closest beacon is at x=15, y=3
    ... Sensor at x=20, y=1: closest beacon is at x=15, y=3
    ... ''', 20)
    56000011
    """

    def manhatten(p1,p2):
        delta = p1 - p2 
        return int(abs(delta.real)+abs(delta.imag))

    sensors = {sensor:manhatten(sensor, beacon) for sensor, beacon in map(parse_line, rawdata.splitlines())}

    possible = []

    for sensor, distance in sensors.items():
        # go round all the points just outside the range of each sensor and see
        # if they're covered by another sensor
        sx,sy = int(sensor.real), int(sensor.imag)
        for dy in range(distance + 2):
            dx = distance + 1 - dy

            for x,y in (sx+dx, sy+dy),\
                       (sx+dx, sy-dy),\
                       (sx-dx, sy+dy),\
                       (sx-dx, sy-dy):

                if not 0 <= x <= max_coord or not 0 <= y <= max_coord:
                    continue

                if not any(manhatten(complex(x,y),s2) <= d2 
                           for s2, d2 in sensors.items()):
                    return x*4000000 + y


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
