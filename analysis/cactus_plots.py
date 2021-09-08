#!/usr/bin/python3

import argparse
import csv
import os
import sys
from functools import reduce
from typing import Dict, Set, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def format_logdecimal(value, pos=None):
    if value < 1:
        return '$%.2f$' % value
    else:
        return '$%d$' % value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This utility takes csv files and creates time and memory cactus plots for them."
    )
    parser.add_argument(
        "-f",
        "--format",
        help="The format of the saved figures. Must be a matplotlib supported format. Defaults to pdf",
        default="pdf",
    )
    parser.add_argument(
        "-l", "--limit", help="Limit the y-axis on the plots.", type=int
    )
    parser.add_argument(
        "-t", "--time_limit", help="Add an artificial time limit in seconds. All queries taking longer than this will be excluded from both the memory and the time plots.", type=float
    )
    parser.add_argument(
        "-m",
        "--min",
        help="Remove all queries that finish faster than this argument in seconds.",
        type=float,
    )
    parser.add_argument(
        "--tail", help="Display only the n last points of the cactus plot", type=int
    )
    parser.add_argument(
        "-I",
        "--intersection",
        help="Only display queries in the intersection of all inputs.",
        action="store_true",
    )
    parser.add_argument("--inputs", nargs="+", help="list of input files")
    parser.add_argument("--names", nargs="*", help="list of labels of the inputs")
    parser.add_argument(
        "--max_line",
        action="store_true",
        help="Prints a vertical line at point of the last point of each data set.",
    )
    parser.add_argument(
        "--weak",
        type=int,
        help="What input contains only weak data. Remove data from the other inputs not in this input.",
    )
    parser.add_argument(
        "--filter",
        type=argparse.FileType("r"),
        help="File containing the names of the queries which the inputs should be filtered to. Could fx. be a list of weak queries.",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="Base file to output to. Will be suffixed with '-time.<format>' and '-memory<format>' respectively. Defaults to dash-concatenated list of names.",
    )
    parser.add_argument(
        "-x",
        "--explored",
        action="store_true",
        help="Generate cactus plot of explored states.",
    )
    parser.add_argument(
        "-v",
        "--virtual-best",
        action="store_true",
        help="Generate series of best score across all input for an idealised solver",
    )
    parser.add_argument("--no-legend", help="Disable plot legend", action="store_true")
    parser.add_argument("--exclude", type=argparse.FileType("r"), help="Exclude queries listed in file")
    args = parser.parse_args()

    if len(args.names) != len(args.inputs):
        print(args.names)
        print(args.inputs)
        raise RuntimeError("Please provide as many names as input files (in order)")

    if args.exclude:
        exclude = set(q.strip() for q in args.exclude.readlines())
    else:
        exclude = set()

    inputs: Dict[str, Dict[str, Tuple[str, float, int, int]]] = {}
    n_inputs = len(args.inputs)
    for name, input in zip(args.names, args.inputs):
        with open(input, "r") as file:
            reader = csv.reader(file)
            inputs[name] = {
                x[0]: (x[1], float(x[2]), int(x[3]), int(x[4]) if len(x) > 4 else 0)
                for x in reader
                if (args.time_limit is None or float(x[2]) <= args.time_limit)
                and x[0] not in exclude
            }

    all_queries: Optional[Set[str]] = None
    if args.intersection:
        all_queries = reduce(
            lambda acc, i: acc.union(set(i.keys())), inputs.values(), set()
        )
        query_intersection: Set[str] = reduce(
            set.intersection, map(lambda x: set(x.keys()), inputs.values())
        )

        to_remove = all_queries - query_intersection

        for query in to_remove:
            for input in inputs.values():
                if query in input:
                    del input[query]

    if args.output_file:
        outfile_base = args.output_file
    else:
        outfile_base = f"{'-'.join(args.names)}"

    if args.virtual_best:
        virtual_best = {}
        if all_queries is None:
            all_queries = reduce(
                lambda acc, i: acc.union(set(i.keys())), inputs.values(), set()
            )
        for query in all_queries:
            answers = [input[query] for input in inputs.values() if query in input.keys()]
            t = min(answer[1] for answer in answers)
            mem = min(answer[2] for answer in answers)
            states = min(answer[3] for answer in answers)
            virtual_best[query] = (query, t, mem, states)
        inputs["Virtual Best Solver"] = virtual_best

    fig, ax = plt.subplots()
    linestyles = ['-', '--', '-.', ':'] * 2 + [(0, (3,1,1,1)), (0, (5, 1)), (0, (3, 3,1,3,1,3))]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] * 2 + ['#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    linewidths = 4 * [1] + 4 * [1.6]

    fig.set_figwidth(7.2)
    fig.set_figheight(4.2)

    vbslinestyle = (0, (5, 2, 1, 2, 1, 2))
    vbscolor = '#000000'
    plt.yscale('log')
    #ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_logdecimal))
    #ax.yaxis.set_minor_formatter(ticker.FuncFormatter(format_logdecimal))
    formatter = ticker.LogFormatter(minor_thresholds=(2,1.5))
    #formatter = ticker.FuncFormatter(format_logdecimal)
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_minor_formatter(formatter)
    x_maxes = []
    time_series = {}
    for i, (name, input) in enumerate(inputs.items()):
        time = sorted(
            [t for _, t, _, _ in input.values() if (args.limit is None or t < args.limit) and (args.min is None or t >= args.min)]
        )
        time_series[name] = time
        x_maxes.append(len(time))
        n_below = len(input.values()) - len(time)

        linestyle = vbslinestyle if name == "Virtual Best Solver" else linestyles[i]
        color = vbscolor if name == "Virtual Best Solver" else colors[i]
        path = plt.plot(range(n_below, n_below + len(time)), time,
                        linestyle=linestyle, linewidth=linewidths[i], color=color, label=f"{name} ")
        # c=path.get_facecolors()[0].tolist()
        if args.max_line:
            plt.axvline(len(time), c='k', linestyle='--')

    x_maxes = sorted(x_maxes)
    if args.tail:
        if args.virtual_best:
            cut = max(x_maxes[:-1]) - args.tail
        else:
            cut = max(x_maxes) - args.tail
        plt.xlim(left=cut, right=max(x_maxes) + 5)
        ybot = 0.8 * min(T[cut] for T in time_series.values())
        ytop = 1.2 * max(T[-1] for T in time_series.values())
        plt.ylim(ybot, ytop)
    else:
        pass
        #plt.xlim(left=plt.xlim()[0] * 0.9)

    if not args.no_legend:
        plt.legend(fontsize='small')
    #plt.title("Time (in seconds)")
    plt.ylabel("Time (s)")
    plt.xlabel("Instances")
    #ax.xaxis.set_label("Instances")
    #ax.yaxis.set_label("Time (in s)")
    if args.limit is not None:
        plt.ylim(top=args.limit)
    if args.min is not None:
        plt.ylim(bottom=args.min)

    #plt.show()
    plt.savefig(f"{outfile_base}-time.{args.format}", format=args.format, bbox_inches="tight", dpi=1000)
    plt.clf()

    sys.exit(0)
    print("Config\t\t\tMedian\tDist to baseline")
    dataset = list(time_series.items())
    for i, (name, input) in enumerate(dataset):
        median = sorted(input)[len(input) // 2]
        prev_base = dataset[i // 4 * 4]
        base = inputs[prev_base[0]]
        sorted_input = sorted([t for _, t, _, _ in inputs[name].values() if args.limit is None or t < args.limit])
        dist_base = sorted_input[len(base) - 1]
        print(f"{name:18}\t{median}\t{dist_base}")

