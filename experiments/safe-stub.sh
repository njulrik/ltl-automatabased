#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "safe-stub" -r "-s DFS --ltl-por reach" reach-stub-new@268 mcc2021
cd experiments
