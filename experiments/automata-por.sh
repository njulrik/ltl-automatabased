#! /bin/bash

if [[ -z $PARTITION ]]; then PARTITION=none; fi
cd ..
./run_job.sh -t 15 -m 16 -p $PARTITION -n "safe-stub" -r "-s DFS --ltl-por reach" verifypn-linux64 mcc2021
cd experiments
