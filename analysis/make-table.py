#!/usr/bin/env python3

import argparse
import os
import sys
import itertools
#from typing import IO, List, Dict
from common import *


if __name__ == "__main__":
    parser = get_argument_parser()
    parser.add_argument("--filename", type=str, help="Filename to write the table to.", default="num-answered.tex")
    args = parse_program_arguments(parser)

    dataset = {}
    for input, name in zip(args.input, args.names):
        dataset[name] = import_csv(input)

    num_answers_table(dataset, args, args.filename)
