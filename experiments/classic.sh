#! /bin/bash

if [[ -z $PARTITION ]]; then PARTITION=none; fi
cd ..
./run_job.sh -t 15 -m 16 -p $PARTITION -n "classic" -r "-s DFS --ltl-por classic" verifypn-linux64 mcc2021
cd experiments
