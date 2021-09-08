#!/usr/bin/env python3

from common import import_csv
import argparse
from glob import glob
import os
import re
import sys

FORMULA_PATTERN = "FORMULA (.*) (TRUE|FALSE) TECHNIQUES"
ans_str = re.compile(FORMULA_PATTERN)

def get_answers(dir, category):
    card = {}
    fire = {}
    for fname in glob(os.path.join(dir, f"*{category}F*")):
        with open(fname, "r") as f:
            res = ans_str.findall(f.read())
            fire.update(set(res))
    for fname in glob(os.path.join(dir, f"*{category}C*")):
        with open(fname, "r") as f:
            res = ans_str.findall(f.read())
            card.update(set(res))

    return {"Cardinality": card, "Fireability": fire}

def main():
    parser = argparse.ArgumentParser(description="Compare results of two parallel experiments. The experiments are specified as the folders containing the raw output from the executions")
    parser.add_argument("left", type=str)
    parser.add_argument("right", type=str)
    parser.add_argument("-x", "--exclusive", action='store_true', help="Print answers exclusive to left side")
    parser.add_argument("-c", "--category", default="LTL", help="The category to check.")

    args = parser.parse_args()

    left = get_answers(args.left, args.category)
    right = get_answers(args.right, args.category)

    if args.exclusive:
        print("Exclusive answers to left")
        for cat in "Cardinality", "Fireability":
            print(f"In {args.category}{cat}:")
            for query in left[cat].keys() - right[cat].keys():
                print(f" {query}")
            print(f"Total (left): {len(left[cat])}.")
            print(f"Total (right): {len(right[cat])}.")
            print(f"Exclusive to left: {len(left[cat].keys() - right[cat].keys())}")

    else:
        printed_header = False
        for cat in "Cardinality", "Fireability":

            print(f"Processing {args.category}{cat}...")
            for query in left[cat].keys() & right[cat].keys():
                if left[cat][query] != right[cat][query]:
                    if not printed_header:
                        printed_header = True
                        print("Mismatching answers:")
                    print(f"  {query}, left says {left[cat][query].answer}")
            if not printed_header:
                print("No mismatching answers")

            print(f"Total answers in {args.category}{cat}:")
            print(f"  Left: {len(left[cat])}")
            print(f"  Right: {len(right[cat])}")
        # TODO LTLF/LTLC distinction

if __name__ == '__main__':
    main()
