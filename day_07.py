#!/usr/bin/env -S pdm run python

class Dir:
    @classmethod
    def parse(cls, listing):
        root = Dir(None)
        current = root
        for line in listing.splitlines():
            match line.split():
                case ["$", "cd", "/"]:
                    current = root
                case ["$", "cd", ".."]:
                    current = current.parent
                case ["$", "cd", target]:
                    current = current.subdirs[target]
                case ["$", "ls"]:
                    continue
                case ["dir", name]:
                    current.subdirs[name] = Dir(current)
                case [size, name]:
                    current.files[name] = int(size)
                case _:
                    raise ValueError(line)

        return root

    def __init__(self, parent):
        self.files = {}
        self.subdirs = {}
        self.parent = parent

    @property
    def size(self):
        return sum(self.files.values()) + sum(d.size for d in self.subdirs.values())

    def walk(self):
        yield self
        for d in self.subdirs.values():
            yield from d.walk()

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... $ cd /
    ... $ ls
    ... dir a
    ... 14848514 b.txt
    ... 8504156 c.dat
    ... dir d
    ... $ cd a
    ... $ ls
    ... dir e
    ... 29116 f
    ... 2557 g
    ... 62596 h.lst
    ... $ cd e
    ... $ ls
    ... 584 i
    ... $ cd ..
    ... $ cd ..
    ... $ cd d
    ... $ ls
    ... 4060174 j
    ... 8033020 d.log
    ... 5626152 d.ext
    ... 7214296 k
    ... ''')
    95437
    """
    root = Dir.parse(rawdata)
    return sum(r.size for r in root.walk() if r.size <= 100000)

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... $ cd /
    ... $ ls
    ... dir a
    ... 14848514 b.txt
    ... 8504156 c.dat
    ... dir d
    ... $ cd a
    ... $ ls
    ... dir e
    ... 29116 f
    ... 2557 g
    ... 62596 h.lst
    ... $ cd e
    ... $ ls
    ... 584 i
    ... $ cd ..
    ... $ cd ..
    ... $ cd d
    ... $ ls
    ... 4060174 j
    ... 8033020 d.log
    ... 5626152 d.ext
    ... 7214296 k
    ... ''')
    24933642
    """
    root = Dir.parse(rawdata)
    needed = 30000000
    current = 70000000 - root.size
    return min(r.size for r in root.walk() if current + r.size >= needed)

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
