#! /usr/bin/env python
import argparse
from datetime import date
import doctest
import importlib
from pathlib import Path
import sys

import aocd
from parse import parse

parser = argparse.ArgumentParser()
parser.add_argument("--no-test", action="store_false", dest="test", help="Skip automated doc test when running. When omitted, the entire module for the selected day is tested even if only one part would actually be run")
parser.add_argument("--no-submit", action="store_false", dest="submit")
parser.add_argument("--day", type=int, choices=range(1,26), help="Omit for today but only during the advent season")
parser.add_argument("--year", type=int, help="Puzzle year. If omitted, detect based on the containing folder name")
parser.add_argument("--part", type=int, choices=[1,2], action="append", help="Which puzzle(s) to run. If omitted, run all that exist in the script for the selected day. Can be used multiple times to explicitly include multiple parts")

args = parser.parse_args()

if args.year is None:
    dirname = Path().absolute().stem
    args.year = parse("aoc-{:d}", dirname)[0]

if args.day is None: 
    today = date.today()
    if (today.month, today.year) != (12, args.year) or not 1 <= today.day <= 25:
        sys.exit(f"Can only guess the day during AOC season {args.year}")

    args.day = today.day

solution_module = importlib.import_module(f'day_{args.day:02}')

if args.test:
    failure, tests = doctest.testmod(solution_module)
    if failure > 0:
        sys.exit(f"Failed {failure}/{tests} tests")

rawdata = aocd.get_data(year=args.year, day=args.day)
parseddata = getattr(solution_module, "_parse")(rawdata)

for part in (args.part or [1,2]):
    try:
        solution = getattr(solution_module, f'part_{part}')(*parseddata)
    except AttributeError:
        # If parts were specified, they must exist, but if we're running all of them 
        if args.part:
            sys.exit(f"Day {args.day} has no solution for part {part}")
        else:
            continue

    print(f"Solution to part {part}: ", solution, sep="\n")

    if args.submit:
        # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
        aocd.submit(solution, year=args.year, day=args.day, part='ab'[part-1], reopen=False)

