# Reproducibility Package: Automata-Driven Partial Order Reduction and Guided Search for LTL
Reproducibility package for the paper *Automata-Driven Partial Order Reduction and Guided Search for LTL Model Checking*, authored by Peter Gjøl Jensen, Jiri Srba, Nikolaj Jensen Ulrik, and Simon Mejlby Virenfeldt, extended from the Master's Thesis by Nikolaj Jensen Ulrik and Simon Mejlby Virenfeldt. 
The package contains the binaries used to obtain the answers contained within the paper, the scripts to run the experiments from the paper, and scripts used for data processing and obtaining the results present in the paper.

## Usage

The data processing scripts assume a Unix-like environment (e.g. Linux) with Bash and Python 3 (3.9.5 tested, however earlier versions may work), and the supplied binaries assume 64-bit Linux.

### Model checker
The binaries are available in `sequential-bin` and `parallel-bin` (supports multicore query simplification, for use in the MCC setup). 
The source code used to create the binaries can be found at Launchpad [here](https://bazaar.launchpad.net/~tapaal-ltl/verifypn/reach-stub-new/revision/268?start_revid=268.). These sources should also be possible to compile for other operating systems (in particular Windows and OSX). 

#### Install dataset
The experiments are run using the MCC 2021 dataset, which is expected to be located in `mcc2021` (one folder per model with all relevant queries). 
If you do not already have the dataset, the script `install_models.sh` will download and install the models appropriately (requires `wget`). 
Alternatively you can download and install the data set yourself ([Download](https://mcc.lip6.fr/archives/INPUTS-2021.tar.gz)). 

#### Single Configuration

1. Run the desired experiment from the `experiments` folder or run `all_experiments.sh`.
2. The answers are available in `output/mcc2020`.

The experiments are by default run using GNU `parallel` (on Ubuntu run `apt-get install parallel`).
If you have a cluster running Slurm, you can specify a partition using the `PARTITION` environment variable.
If you have a cluster running a different scheduler, you will need to modify the `run_*.sh` scripts yourself.

#### MCC setup

1. Run `run_mcc.sh`.
2. The answers are now available in the `BENCHKIT` folder.

The experiments are by default run using GNU `parallel` (on Ubuntu run `apt-get install parallel`).
If you have a cluster running Slurm, you can specify a partition using the `PARTITION` environment variable.
If you have a cluster running a different scheduler, you will need to modify the `run_*.sh` scripts yourself.

### Data analysis (Single core)
Data analysis is done using various Python 3 scripts located in `analysis`. All scripts (excluding `common.py`) have usage strings via `-h` (e.g. `python analysis/to_csv.py -h` or equivalently `analysis/to_csv.py -h`), which may contain more options than detailed here.

#### Using our results

The raw data from our thesis is available in the two files `output.tar.gz` and `BENCHKIT.tar.gz`. Extract these files to perform data analysis on our results (1.8 GiB when unpacked).
For data analysis on your own data, simply proceed to the next step.

``` sh
$ tar -xzf output.tar.gz && tar -xzf BENCHKIT.tar.gz
```

#### Preprocessing

For processing the files obtained from single-query experiments, our scripts assume a CSV representation obtainable via `to_csv.py`. 
If the raw results are located in `output/mcc2020/foo`, `python analysis/to_csv.py output/mcc2020/foo` will write the CSV representation to stdout, which we recommend redirecting to a file like so:

``` sh
$ python analysis/to_csv.py output/mcc2020/foo > csv/foo.csv
```

The CSV representation contains (in order) the formula name, the answer (`TRUE` or `FALSE`), the time taken (in seconds) and peak memory usage (in KB).
Each line corresponds to one answer, thus the total number of answers can be found using `wc -l csv/foo.csv`.

#### Computing "interesting" instances

For ease of presentation, the figures in the paper do not include all 37792 queries in the MCC 2021 states since a massive number of these are straightforward to solve with any technique.
We consider as interesting those queries that took more than 30 seconds for the baseline to solve and was solved by any configuration present.
To compute the queries to exclude from consideration, run, e.g. 

``` sh
$ python analysis/aggregate-files.py csv/foo.csv csv/bar.csv > exclude
```

The first file listed is treated as baseline file, thus in the above example the interesting queries would be those that took configuration `foo` more than 30 seconds to solve but were solved by either of `foo` and/or `bar`.

Naturally you can specify your own list of queries to exclude. Make sure that the queries in your file also contain the `-LTLC` or `-LTLF` suffix if relevant, i.e. they correspond to query names in the .csv files, otherwise nothing will be excluded.

#### Tables

The tables are output to `.tex` files containing just a `tabular` environment. The tables depend on the `siunitx` package. To modify the style or contents of the tables (e.g. if you want to avoid the `siunitx` dependency), you will need to modify `analysis/common.py`.

A tables is generated from a list of inputs and a list of row names, which are paired up (both must have the same length!).
For example, a table with rows Foo and Bar can be generated from `foo.csv` and `bar.csv` with

``` sh
$ python analysis/make-table.py --inputs foo.csv bar.csv --names Foo Bar -o foo-bar-answered.tex
```

To exclude answers (e.g. to limit numbers to instances of interest), use the `-x/--exclude` option with a filename.

#### Plots

The cactus plots are generated using `analysis/cactus_plots.py` (depends on `matplotlib` (tested using version 3.4.1), and a usable `pdflatex` for TeX fonts).
Like `make-table.py`, the cactus plots are given a list of CSV files and a list of labels.
In the thesis, for each comparison there is a cactus plot with a minimum time of 1 second and a cactus plot showing the top 1500 indices, obtainable as follows:

``` sh
python analysis/cactus_plots.py --input $INPUTS --names $NAMES --virtual-best -o cactus-all --no-simplification -m 1
python analysis/cactus_plots.py --input $INPUTS --names $NAMES --virtual-best -o cactus-tail --no-simplification --tail 1500 --no-legend
```

By defauls the plots are output as .pdf files. This can be modified using the `-f/--format` option (see the documentation for `matplotlib.pyplot.savefig` for valid formats).

**NOTE:** The present version of the script assumes you want to create the version in the paper, which has two sets of 4 lines in one plot. 
If you want to plot a different number of lines, you'll want to tweak some of the styling parameters starting from line 148 (the `linestyles`, `colours`, and `linewidths` variables), or your plot might display strangely.

The particular plot used in the paper is computed as follows (after running `analysis/aggregate-files.py` as described above):

``` sh
python analysis/cactus_plots.py --inputs csv/{baseline,classic,liebke,state-por,heur+baseline,heur+classic,heur+liebke,heur+state-por} --names "Baseline" Classic "Automata-driven POR" "Liebke POR" "Baseline Heur" "Classic HPOR" "Automata-driven HPOR" "Liebke HPOR" --exclude analysis/generated/exclude -o cactus.pdf -m 45
```

### Data analysis (multicore)

The multicore data analysis is slightly more complicated, as the same query can be potentially answered multiple times. 
The script `analysis/check_benchkit.py` compares two multicore experiments and prints number of answers for each.
Further data analysis opportunities are limited, as the experimental set-up does not provide easy access to running time or peak memory consumption.
