#!/usr/bin/env -S pdm run python
import functools
import itertools as it

Packet = "list[int|'Packet']"

def in_order(left:Packet, right:Packet):
    for l, r in zip(left, right):
        match l,r:
            case int(), int() if l != r:
                return l < r
            case list(), list() if l != r:
                return in_order(l,r)
            case int(), list():
                return in_order([l], r)
            case list(), int():
                return in_order(l, [r])

    return len(left) <= len(right)

def packets(rawdata:str):
    pairs = rawdata.split("\n\n")
    def packet(lines:str):
        left, right = lines.splitlines()
        return eval(left), eval(right)

    return [packet(pair) for pair in pairs]

def part_1(rawdata:str):
    r"""
    >>> part_1('''\
    ... [1,1,3,1,1]
    ... [1,1,5,1,1]
    ... 
    ... [[1],[2,3,4]]
    ... [[1],4]
    ... 
    ... [9]
    ... [[8,7,6]]
    ... 
    ... [[4,4],4,4]
    ... [[4,4],4,4,4]
    ... 
    ... [7,7,7,7]
    ... [7,7,7]
    ... 
    ... []
    ... [3]
    ... 
    ... [[[]]]
    ... [[]]
    ... 
    ... [1,[2,[3,[4,[5,6,7]]]],8,9]
    ... [1,[2,[3,[4,[5,6,0]]]],8,9]
    ... ''')
    13
    """
    return sum(i for i,(l,r) in enumerate(packets(rawdata), start=1) if in_order(l,r))    

def part_2(rawdata:str):
    r"""
    >>> part_2('''\
    ... [1,1,3,1,1]
    ... [1,1,5,1,1]
    ... 
    ... [[1],[2,3,4]]
    ... [[1],4]
    ... 
    ... [9]
    ... [[8,7,6]]
    ... 
    ... [[4,4],4,4]
    ... [[4,4],4,4,4]
    ... 
    ... [7,7,7,7]
    ... [7,7,7]
    ... 
    ... []
    ... [3]
    ... 
    ... [[[]]]
    ... [[]]
    ... 
    ... [1,[2,[3,[4,[5,6,7]]]],8,9]
    ... [1,[2,[3,[4,[5,6,0]]]],8,9]
    ... ''')
    140
    """
 
    @functools.total_ordering
    class SortablePacket:
        def __init__(self, p:Packet):
            self.p = p

        def __eq__(self, other):
            return self.p == other.p

        def __le__(self, other):
            return in_order(self.p, other.p)
   
    divider_1 = [[2]]
    divider_2 = [[6]]

    orig_packets = list(it.chain.from_iterable(packets(rawdata)))
    sorted_packets = sorted(orig_packets+[divider_1, divider_2], key=SortablePacket)

    return (sorted_packets.index(divider_1)+1) * (sorted_packets.index(divider_2)+1)

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
