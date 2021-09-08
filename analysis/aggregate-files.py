#!/usr/bin/env python3


from common import *
import os
import sys
from copy import copy
from glob import glob
import re
import locale
import functools
from plot_keys import max_time, t_lower_bound

import argparse

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} [CSV-files...]")
    print("Assumes first file denotes the baseline configuration (which is treated differently)")
    sys.exit(0)


# the all-queries file was computed via bash-fu in the mcc2021 directory:
# $ find mcc2021 -name "LTLC*.xml" | xargs grep "<id>.*PT.*" | awk '{print $2 "-LTLC"}' | sed -E "s#</?id>##g" | sort > scripts/all-ltlc
# produces all LTLCardinality queries. Do similarly for LTLFireability, then do
# $ cat all-ltlc all-ltlf | sort | uniq > all-queries

with open(f"{os.path.dirname(sys.argv[0])}/all-queries") as f:
    all_queries = set(q.strip() for q in f.readlines())
maxt = max_time
threshold_time = t_lower_bound

csvs = []
for filename in sys.argv[1:]:
    with open(filename) as f:
        csvs.append({key: row for key, row in import_csv(f).items() if row.time <= maxt})


any_solved = set()
for dataset in csvs:
    any_solved = any_solved.union(dataset.keys())


all_solved = copy(any_solved)
for dataset in csvs:
    all_solved = all_solved.intersection(set(dataset.keys()))
    all_solved = {key for key in all_solved if dataset[key].time <= threshold_time}
    for key in all_solved:
        if dataset[key].time > threshold_time:
            all_solved.remove(key)

all_solved_threshold = {key for key in csvs[0].keys() if csvs[0][key].time <= threshold_time}
all_solved = set(csvs[0].keys()) #{key for key in any_solved if all(map(lambda data: key in data, csvs))}

none_solved = all_queries - any_solved

exclude = all_solved_threshold | none_solved


# locale hacking to make the files play nice with POSIX comm if needed (otherwise Python sorts it strangely)
# input your own locale as needed if you have this requirement
#locale.setlocale(locale.LC_ALL, 'en_DK.UTF-8')
outpath = os.path.join(os.path.dirname(sys.argv[0]), "generated")
with open(f'{outpath}/any-solved', 'w') as f:
    for key in sorted(any_solved, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open(f'{outpath}/all-solved', 'w') as f:
    for key in sorted(all_solved, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open(f'{outpath}/none-solved', 'w') as f:
    for key in sorted(none_solved, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open(f'{outpath}/exclude', 'w') as f:
    for key in sorted(exclude, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open(f'{outpath}/table-total', "w") as f:
    print(f"\\num{{{len(all_queries) - len(exclude)}}}", file=f, end="")

with open(f'{outpath}/table-threshold', "w") as f:
    print(f"\\SI{{{threshold_time}}}{{\\second}}", file=f, end="")

#with open(f'{outpath}/plot-threshold", "w") as f:
#    print(f"\\si{{{threshold_time}}}{{\\second}}", file=f, end="")
