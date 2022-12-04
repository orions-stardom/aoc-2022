from parse import parse

def _parse(rawdata):
    return [parse("{:d}-{:d},{:d}-{:d}", line.strip()) for line in rawdata.splitlines()]

def part_1(*lines):
    r"""
    >>> part_1(*_parse('''\
    ... 2-4,6-8
    ... 2-3,4-5
    ... 5-7,7-9
    ... 2-8,3-7
    ... 6-6,4-6
    ... 2-6,4-8    
    ... '''))
    2
    """
    return sum((a>=c and b<=d) or (c>=a and d<=b) for a,b,c,d in lines)


def part_2(*lines):
    r"""
    >>> part_2(*_parse('''\
    ... 2-4,6-8
    ... 2-3,4-5
    ... 5-7,7-9
    ... 2-8,3-7
    ... 6-6,4-6
    ... 2-6,4-8    
    ... '''))
    4
    """
    return sum(bool(set(range(a,b+1))&set(range(c,d+1))) for a,b,c,d in lines)
