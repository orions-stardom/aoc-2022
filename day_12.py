#!/usr/bin/env -S pdm run python
import networkx as nx

def height_map(rawdata:str):
    elevation = {}
    for y,line in enumerate(rawdata.splitlines()):
        for x,c in enumerate(line):
            coord = complex(x,y)
            if c == "S":
                start = coord
                c = "a"
            elif c == "E":
                end = coord
                c = "z"
            elevation[coord] = ord(c) - ord("a")

    graph = nx.DiGraph()

    for point in elevation:
        for dz in 1,-1,1j,-1j:
            if point+dz in elevation:
                climb = elevation[point+dz] - elevation[point]
                if climb > 1:
                    continue
                graph.add_edge(point,point+dz)

    return graph, start, end, elevation

def part_1(rawdata:str):
    r"""
    >>> part_1('''\
    ... Sabqponm
    ... abcryxxl
    ... accszExk
    ... acctuvwj
    ... abdefghi
    ... ''')
    31
    """
    graph, start, end, _ = height_map(rawdata)
    return nx.shortest_path_length(graph, start, end)


def part_2(rawdata:str):
    r"""
    >>> part_2('''\
    ... Sabqponm
    ... abcryxxl
    ... accszExk
    ... acctuvwj
    ... abdefghi
    ... ''')
    29
    """
    graph, _, end, elevation = height_map(rawdata)
    cands = [coord for coord in elevation if elevation[coord] == 0]

    # cant just pass it to min() because some candidate starts have no path
    minlength = float("inf")
    for cand in cands:
        try:
            length = nx.shortest_path_length(graph, cand, end)
        except:
            continue

        minlength = min(minlength, length)

    return minlength

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
