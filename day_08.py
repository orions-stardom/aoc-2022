#!/usr/bin/env -S pdm run python
import numpy as np
import itertools as it
import more_itertools as mit

def parse_grid(rawdata):
    return np.array([[int(x) for x in line] for line in rawdata.splitlines()])

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... 30373
    ... 25512
    ... 65332
    ... 33549
    ... 35390
    ... ''')
    21
    """
    trees = parse_grid(rawdata)
    def is_visible(x,y,h):
        return np.all(trees[:x,y] < h) or np.all(trees[x+1:,y] < h) or np.all(trees[x,:y] < h) or np.all(trees[x,y+1:] < h)
        
    return sum(is_visible(x,y,h) for (x,y),h in np.ndenumerate(trees)) 

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... 30373
    ... 25512
    ... 65332
    ... 33549
    ... 35390
    ... ''')
    8
    """
    def scenic_score(idx,h):
        def n_visible(direction):
            n = 0
            cand = idx + direction
            while np.all(((0,0) <= cand) & (cand < trees.shape)):
                n += 1
                if trees[*cand] >= h:
                    break
                cand += direction

            return n
        
        return n_visible(np.array((0,1))) * n_visible(np.array((0,-1))) * n_visible(np.array((1, 0))) * n_visible(np.array((-1, 0)))
    
    trees = parse_grid(rawdata)
    return max(scenic_score(idx,h) for idx,h in np.ndenumerate(trees)) 

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
