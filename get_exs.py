#!/usr/bin/env python3

"""
Randomly select next exercises from cracking the coding interview 6ed.
"""

import json
import argparse
import random
import glob
import os

DONE_EXS_DIR_PATH = "./problems"

#exercise set of the book
EXS = {
    1: set(range(1, 9+1)),
    2: set(range(1, 8+1)),
    3: set(range(1, 6+1)),
    4: set(range(1, 12+1)),
    5: set(range(1, 8+1)),
    6: set(range(1, 10+1)),
    7: set(range(1, 12+1)),
    8: set(range(1, 14+1)),
    9: set(range(1, 8+1)),
    10: set(range(1, 11+1)),
    11: set(range(1, 6+1)),
    12: set(range(1, 11+1)),
    13: set(range(1, 8+1)),
    14: set(range(1, 7+1)),
    15: set(range(1, 7+1)),
    16: set(range(1, 26+1)),
    17: set(range(1, 26+1)),
}

#chapters organized by groups
EXS_GROUPS = {
    "data_structures": {1, 2, 3, 4},
    "concepts_and_algorithms": {5, 6, 7, 8, 9, 10, 11},
    "knowledge_based": {12, 13, 14, 15},
    "moderate": {16},
    "hard": {17},
}

CHAPTERS = set(EXS.keys())

RANDOM_SEED = 42

def flatten(iterable):
    return [item for group in iterable for item in group]

def error(*args, **kwargs):
    print("ERROR:", *args, **kwargs)
    exit()

def get_done_exs_sets():
    done = {c: set() for c in CHAPTERS}
    paths = glob.glob(os.path.join(DONE_EXS_DIR_PATH, "ch*_ex*.py"))
    for path in paths:
        chapter, ex = os.path.basename(path).split(".")[0].split("_")
        chapter, ex = int(chapter[2:]), int(ex[2:])
        done[chapter].add(ex)
    return done

def get_exs_sets(use_done=False):
    exs = dict(EXS)
    if not use_done:
        done_exs = get_done_exs_sets()
        for c in exs:
            exs[c] -= done_exs[c]
    return exs

def main():
    random.seed(RANDOM_SEED)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        nargs="?",
        type=int,
        help="number of exercises to get",
        default=1
    )
    parser.add_argument(
        "--from_chapters",
        nargs="*",
        choices=CHAPTERS,
        type=int,
        help="select from these chapters only",
        default=None
    )
    parser.add_argument(
        "--exclude_chapters",
        nargs="*",
        choices=CHAPTERS,
        type=int,
        help="exclude these chapters",
        default=set()
    )
    parser.add_argument(
        "--from_groups",
        nargs="*",
        choices=EXS_GROUPS.keys(),
        help="select from these groups only",
        default=EXS_GROUPS.keys()
    )
    parser.add_argument(
        "--exclude_groups",
        nargs="*",
        choices=EXS_GROUPS.keys(),
        help="exclude these groups",
        default=set(),
    )
    parser.add_argument(
        "--use_done",
        nargs="?",
        help="use exercises done in '{}' also".format(DONE_EXS_DIR_PATH),
        const=True,
        default=False
    )
    args = parser.parse_args()

    #getting chapters to get exercises from
    if args.from_chapters is not None:
        chapters = set(args.from_chapters)
    else:
        groups = set(args.from_groups) - set(args.exclude_groups)
        chapters = set(flatten(EXS_GROUPS[g] for g in groups))
    chapters -= set(args.exclude_chapters)
    if not chapters:
        error("empty set of chapters chosen")

    #loading exercises sets
    exs_sets = get_exs_sets(args.use_done)

    #getting exercises to do
    all_exs = flatten([(c, e) for e in exs_sets[c]] for c in chapters)

    #selecting random sample
    exs = random.sample(all_exs, min(args.n, len(all_exs)))

    #printing
    print("{} available exercises from chapters {}.".format(
        len(all_exs), chapters))
    if not exs:
        return

    print("You got {} exercise{}:".format(len(exs), (len(exs) > 1)*"s"))
    for chapter, ex in sorted(exs):
        print("\tchapter {}, exercise {}".format(chapter, ex))

if __name__ == "__main__":
    main()
