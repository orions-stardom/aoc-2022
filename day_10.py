#!/usr/bin/env -S pdm run python

def _parse(rawdata):
    return rawdata.splitlines() 

class Device:
    def __init__(self, instructions):
        self.X = 1
        self.cycle = 0
        self.total_signal = 0

        self.pixels = [["."]*40 for _ in range(6)]

        for instruction in instructions:
            if instruction == "noop":
                self.run_cycle()
            elif instruction.startswith("addx"):
                self.run_cycle()
                self.run_cycle()
                self.X += int(instruction.removeprefix("addx "))
            else:
                raise NotImplementedError

    def run_cycle(self):
        self.cycle += 1
        
        if self.cycle % 40 == 20:
            self.total_signal += self.cycle * self.X

        sprite = (self.X - 1, self.X, self.X + 1)
        draw_y, draw_x = divmod(self.cycle-1, 40)
        self.pixels[draw_y][draw_x] = "#" if draw_x in sprite else "."

    @property
    def picture(self):
        return "\n".join("".join(row) for row in self.pixels)

def part_1(*lines):
    r"""
    >>> part_1(*_parse('''\
    ... addx 15
    ... addx -11
    ... addx 6
    ... addx -3
    ... addx 5
    ... addx -1
    ... addx -8
    ... addx 13
    ... addx 4
    ... noop
    ... addx -1
    ... addx 5
    ... addx -1
    ... addx 5
    ... addx -1
    ... addx 5
    ... addx -1
    ... addx 5
    ... addx -1
    ... addx -35
    ... addx 1
    ... addx 24
    ... addx -19
    ... addx 1
    ... addx 16
    ... addx -11
    ... noop
    ... noop
    ... addx 21
    ... addx -15
    ... noop
    ... noop
    ... addx -3
    ... addx 9
    ... addx 1
    ... addx -3
    ... addx 8
    ... addx 1
    ... addx 5
    ... noop
    ... noop
    ... noop
    ... noop
    ... noop
    ... addx -36
    ... noop
    ... addx 1
    ... addx 7
    ... noop
    ... noop
    ... noop
    ... addx 2
    ... addx 6
    ... noop
    ... noop
    ... noop
    ... noop
    ... noop
    ... addx 1
    ... noop
    ... noop
    ... addx 7
    ... addx 1
    ... noop
    ... addx -13
    ... addx 13
    ... addx 7
    ... noop
    ... addx 1
    ... addx -33
    ... noop
    ... noop
    ... noop
    ... addx 2
    ... noop
    ... noop
    ... noop
    ... addx 8
    ... noop
    ... addx -1
    ... addx 2
    ... addx 1
    ... noop
    ... addx 17
    ... addx -9
    ... addx 1
    ... addx 1
    ... addx -3
    ... addx 11
    ... noop
    ... noop
    ... addx 1
    ... noop
    ... addx 1
    ... noop
    ... noop
    ... addx -13
    ... addx -19
    ... addx 1
    ... addx 3
    ... addx 26
    ... addx -30
    ... addx 12
    ... addx -1
    ... addx 3
    ... addx 1
    ... noop
    ... noop
    ... noop
    ... addx -9
    ... addx 18
    ... addx 1
    ... addx 2
    ... noop
    ... noop
    ... addx 9
    ... noop
    ... noop
    ... noop
    ... addx -1
    ... addx 2
    ... addx -37
    ... addx 1
    ... addx 3
    ... noop
    ... addx 15
    ... addx -21
    ... addx 22
    ... addx -6
    ... addx 1
    ... noop
    ... addx 2
    ... addx 1
    ... noop
    ... addx -10
    ... noop
    ... noop
    ... addx 20
    ... addx 1
    ... addx 2
    ... addx 2
    ... addx -6
    ... addx -11
    ... noop
    ... noop
    ... noop
    ... '''))
    13140
    """
    return Device(lines).total_signal


def part_2(*lines):
    r"""
    >>> part_2(*_parse('''\
    ... addx 15
    ... addx -11
    ... addx 6
    ... addx -3
    ... addx 5
    ... addx -1
    ... addx -8
    ... addx 13
    ... addx 4
    ... noop
    ... addx -1
    ... addx 5
    ... addx -1
    ... addx 5
    ... addx -1
    ... addx 5
    ... addx -1
    ... addx 5
    ... addx -1
    ... addx -35
    ... addx 1
    ... addx 24
    ... addx -19
    ... addx 1
    ... addx 16
    ... addx -11
    ... noop
    ... noop
    ... addx 21
    ... addx -15
    ... noop
    ... noop
    ... addx -3
    ... addx 9
    ... addx 1
    ... addx -3
    ... addx 8
    ... addx 1
    ... addx 5
    ... noop
    ... noop
    ... noop
    ... noop
    ... noop
    ... addx -36
    ... noop
    ... addx 1
    ... addx 7
    ... noop
    ... noop
    ... noop
    ... addx 2
    ... addx 6
    ... noop
    ... noop
    ... noop
    ... noop
    ... noop
    ... addx 1
    ... noop
    ... noop
    ... addx 7
    ... addx 1
    ... noop
    ... addx -13
    ... addx 13
    ... addx 7
    ... noop
    ... addx 1
    ... addx -33
    ... noop
    ... noop
    ... noop
    ... addx 2
    ... noop
    ... noop
    ... noop
    ... addx 8
    ... noop
    ... addx -1
    ... addx 2
    ... addx 1
    ... noop
    ... addx 17
    ... addx -9
    ... addx 1
    ... addx 1
    ... addx -3
    ... addx 11
    ... noop
    ... noop
    ... addx 1
    ... noop
    ... addx 1
    ... noop
    ... noop
    ... addx -13
    ... addx -19
    ... addx 1
    ... addx 3
    ... addx 26
    ... addx -30
    ... addx 12
    ... addx -1
    ... addx 3
    ... addx 1
    ... noop
    ... noop
    ... noop
    ... addx -9
    ... addx 18
    ... addx 1
    ... addx 2
    ... noop
    ... noop
    ... addx 9
    ... noop
    ... noop
    ... noop
    ... addx -1
    ... addx 2
    ... addx -37
    ... addx 1
    ... addx 3
    ... noop
    ... addx 15
    ... addx -21
    ... addx 22
    ... addx -6
    ... addx 1
    ... noop
    ... addx 2
    ... addx 1
    ... noop
    ... addx -10
    ... noop
    ... noop
    ... addx 20
    ... addx 1
    ... addx 2
    ... addx 2
    ... addx -6
    ... addx -11
    ... noop
    ... noop
    ... noop
    ... '''))
    ##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######.....
    """
    print(Device(lines).picture)

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
        if solution is not None:
            print(f"Solution to part {part}: ", solution, sep="\n")
            # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
            aocd.submit(solution, part='ab'[part-1], reopen=False)
        else:
            print("No solution to part {part} {might need to be entered manually?)")
