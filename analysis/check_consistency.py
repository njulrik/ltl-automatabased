#!/usr/bin/env python3

from common import import_csv
import argparse

def main():
    parser = argparse.ArgumentParser(description="Checks for consistency between two experiments in .csv format.")
    parser.add_argument("left", type=argparse.FileType("r"))
    parser.add_argument("right", type=argparse.FileType("r"))
    parser.add_argument("-x", "--exclusive", action='store_true', help="Print answers exclusive to left side")

    args = parser.parse_args()

    left = import_csv(args.left)
    right = import_csv(args.right)

    if args.exclusive:
        print("Exclusive answers to left:")
        for query in left.keys() - right.keys():
            print(f"  {query}")
    else:
        printed_header = False
        for query in left.keys() & right.keys():
            if left[query].answer != right[query].answer:
                if not printed_header:
                    printed_header = True
                    print("Mismatching answers:")
                print(f"  {query}, left says {left[query].answer}")

        if not printed_header:
            print("No mismatching answers")

if __name__ == '__main__':
    main()
