#!/bin/bash

if [[ -z $PARTITION ]]; then PARTITION=none; fi
cd ..
./run_job.sh -t 15 -m 16 -n "torsten+heur" -p $PARTITION -r "-s BestFS --ltl-heur aut --ltl-por automaton" verifypn-linux64 mcc2021
cd experiments
