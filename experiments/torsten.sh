#!/bin/bash

if [[ -z $PARTITION ]]; then PARTITION=none; fi
cd ..
./run_job.sh -t 15 -m 16 -n torsten -p $PARTITION -r "-s DFS --ltl-por automaton" verifypn-linux64 mcc2021
cd experiments
