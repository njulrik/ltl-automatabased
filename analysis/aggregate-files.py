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

pattern = re.compile(r"<id>(.*PT.*)<\/id>")
all_queries = set()
for name in glob(f"{sys.argv[1]}/*-PT-*/LTL*.xml"):
    with open(name) as f:
        res = re.findall(pattern, f.read())
        if "Cardinality" in name:
            res = set(map(lambda n: n + "-LTLC", res))
        elif "Fireability" in name:
            res = set(map(lambda n: n + "-LTLF", res))
        all_queries |= res

maxt = max_time
threshold_time = t_lower_bound

csvs = []
for filename in sys.argv[2:]:
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

exclude_table = all_solved_threshold | none_solved
exclude_plot = all_solved | none_solved


locale.setlocale(locale.LC_ALL, 'en_DK.UTF-8')
with open('table/any-solved', 'w') as f:
    for key in sorted(any_solved, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open('table/all-solved', 'w') as f:
    for key in sorted(all_solved, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open('table/none-solved', 'w') as f:
    for key in sorted(none_solved, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open('table/all-queries', 'w') as f:
    for key in sorted(all_queries, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open('table/exclude-table', 'w') as f:
    for key in sorted(exclude_table, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open('table/exclude-plot', 'w') as f:
    for key in sorted(exclude_plot, key=functools.cmp_to_key(locale.strcoll)):
        print(key, file=f)

with open("table/table-total", "w") as f:
    print(f"\\num{{{len(all_queries) - len(exclude_table)}}}", file=f, end="")

with open("table/table-threshold", "w") as f:
    print(f"\\SI{{{threshold_time}}}{{\\second}}", file=f, end="")

with open("table/plot-total", "w") as f:
    print(f"\\num{{{len(all_queries) - len(exclude_plot)}}}", file=f, end="")

filtered = []
print("Config\t\t\tMedian\tAverage\tDist to baseline")
for i in range(len(csvs)):
    csv = csvs[i]
    T = sorted([row.time for key, row in csv.items() if key not in exclude_table])
    filtered.append(T)
    prev_base = filtered[i // 4 * 4]
    median = T[len(T) // 2]
    average = sum(T) / len(T)
    dist_base = T[len(prev_base) - 1]

    print(f"{sys.argv[i+2].split('/')[1]:16}\t{median}\t{average:.4}\t{dist_base}")


#with open("table/plot-threshold", "w") as f:
#    print(f"\\si{{{threshold_time}}}{{\\second}}", file=f, end="")
