import more_itertools as mit
import string

def _parse(rawdata):
    return [l.strip() for l in rawdata.splitlines()]

def part_1(*rucksacks):
    r"""
    >>> part_1(*_parse('''\
    ... vJrwpWtwJgWrhcsFMMfFFhFp
    ... jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    ... PmmdzqPrVvPwwTWBwg
    ... wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ... ttgJtRGJQctTZtZT
    ... CrZsJsPPZsGzwwsLwLmpwMDw    
    ... '''))
    157
    """
    def split(rucksack):
        size = len(rucksack)//2
        return rucksack[:size], rucksack[size:]
    def common(r1, r2):
        return mit.only(set(r1) & set(r2))
    return sum(string.ascii_letters.index(common(*r))+1 for r in map(split, rucksacks))


def part_2(*rucksacks):
    r"""
    >>> part_2(*_parse('''\
    ... vJrwpWtwJgWrhcsFMMfFFhFp
    ... jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    ... PmmdzqPrVvPwwTWBwg
    ... wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ... ttgJtRGJQctTZtZT
    ... CrZsJsPPZsGzwwsLwLmpwMDw    
    ... '''))
    70
    """
    def common(r1, r2, r3):
        return mit.only(set(r1) & set(r2) & set(r3))

    return sum(string.ascii_letters.index(common(*g))+1 for g in mit.chunked(rucksacks, 3))

