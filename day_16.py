#!/usr/bin/env -S pdm run python
from dataclasses import dataclass
from parse import parse
from functools import cache
import networkx as nx
import itertools as it

def parse_line(line:str) -> tuple[str,int,list[str]]:
    """
    >>> parse_line("Valve AA has flow rate=0; tunnels lead to valves DD, II, BB")
    ('AA', 0, ['DD', 'II', 'BB'])
    >>> parse_line("Valve JJ has flow rate=21; tunnel leads to valve II")
    ('JJ', 21, ['II'])
    """
    try:
        valve, rate, tunnels = parse("Valve {} has flow rate={:n}; tunnels lead to valves {}", line)
        return valve, rate, tunnels.split(", ")
    except TypeError:
        valve, rate, tunnel = parse("Valve {} has flow rate={:n}; tunnel leads to valve {}", line)
        return valve, rate, [tunnel]

def build_graph(rawdata:str) -> nx.Graph:
    graph = nx.Graph()

    for valve, rate, dests in map(parse_line, rawdata.splitlines()):
        graph.add_node(valve, rate=rate)
        graph.add_edges_from((valve,othervalve) for othervalve in dests)

    return graph

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    ... Valve BB has flow rate=13; tunnels lead to valves CC, AA
    ... Valve CC has flow rate=2; tunnels lead to valves DD, BB
    ... Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
    ... Valve EE has flow rate=3; tunnels lead to valves FF, DD
    ... Valve FF has flow rate=0; tunnels lead to valves EE, GG
    ... Valve GG has flow rate=0; tunnels lead to valves FF, HH
    ... Valve HH has flow rate=22; tunnel leads to valve GG
    ... Valve II has flow rate=0; tunnels lead to valves AA, JJ
    ... Valve JJ has flow rate=21; tunnel leads to valve II
    ... ''')
    1651
    """
    graph = build_graph(rawdata)

    @cache
    def max_flow(open_valves, current_position, minutes_left) -> int:
        if minutes_left == 0:
            return 0

        flow_this_minute = sum(graph.nodes[v]["rate"] for v in open_valves)

        best_so_far = 0
        if current_position not in open_valves and graph.nodes[current_position]["rate"] > 0:
            best_so_far = max_flow(open_valves|{current_position},current_position,minutes_left-1)
    
        for to_valve in graph[current_position]:
            consider = max_flow(open_valves, to_valve, minutes_left-1)
            best_so_far = max(best_so_far, consider)

        return best_so_far + flow_this_minute

    return max_flow(frozenset(), "AA", 30)


def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    ... Valve BB has flow rate=13; tunnels lead to valves CC, AA
    ... Valve CC has flow rate=2; tunnels lead to valves DD, BB
    ... Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
    ... Valve EE has flow rate=3; tunnels lead to valves FF, DD
    ... Valve FF has flow rate=0; tunnels lead to valves EE, GG
    ... Valve GG has flow rate=0; tunnels lead to valves FF, HH
    ... Valve HH has flow rate=22; tunnel leads to valve GG
    ... Valve II has flow rate=0; tunnels lead to valves AA, JJ
    ... Valve JJ has flow rate=21; tunnel leads to valve II
    ... ''')
    1707
    """
    graph = build_graph(rawdata)

    # cache things manually so we can treat you/elephant positions interchangably
    cache = {}
    def max_flow(open_valves, you, elephant, minutes_left) -> int:
        if minutes_left == 0:
            return 0
        if (state := (open_valves, you, elephant, minutes_left)) in cache:
            return cache[state]
        if (state := (open_valves, elephant, you, minutes_left)) in cache:
            return cache[state]

        flow_this_minute = sum(graph.nodes[v]["rate"] for v in open_valves)

        best_so_far = 0
        you_can_open = you not in open_valves and graph.nodes[you]["rate"] > 0
        elephant_can_open = elephant not in open_valves and graph.nodes[elephant]["rate"] > 0

        if you_can_open and elephant_can_open and you != elephant:
            best_so_far = max_flow(open_valves|{you, elephant}, you, elephant, minutes_left-1)
        
        if you_can_open:
            for to_valve in graph[elephant]:
                consider = max_flow(open_valves|{you}, you, to_valve, minutes_left-1)
                best_so_far = max(best_so_far, consider)

        if elephant_can_open:
            for to_valve in graph[you]:
                consider = max_flow(open_valves|{elephant}, to_valve, elephant, minutes_left-1)
                best_so_far = max(best_so_far, consider)

        for you_to, elephant_to in it.product(graph[you], graph[elephant]):
            consider = max_flow(open_valves, you_to, elephant_to, minutes_left-1)
            best_so_far = max(best_so_far, consider)

        result = best_so_far + flow_this_minute
        cache[open_valves,you,elephant,minutes_left] = result
        return result

    return max_flow(frozenset(), "AA", "AA", 26)

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
