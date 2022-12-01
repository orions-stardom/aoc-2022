import heapq

def _parse(rawdata):
    return [[int(x) for x in group.splitlines()] for group in rawdata.split("\n\n")]

def part_1(*elves):
    r"""
    >>> part_1(*_parse('''\
    ... 1000
    ... 2000
    ... 3000
    ...
    ... 4000
    ...
    ... 5000
    ... 6000
    ...
    ... 7000
    ... 8000
    ... 9000
    ...
    ... 10000
    ... '''))
    24000
    """
    return max(sum(e) for e in elves)

def part_2(*elves):
    r"""
    >>> part_2(*_parse('''\
    ... 1000
    ... 2000
    ... 3000
    ...
    ... 4000
    ...
    ... 5000
    ... 6000
    ...
    ... 7000
    ... 8000
    ... 9000
    ...
    ... 10000
    ... '''))
    45000
    """
    return sum(heapq.nlargest(3, (sum(e) for e in elves)))
