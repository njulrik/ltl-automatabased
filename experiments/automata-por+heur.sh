#! /bin/bash

if [[ -z $PARTITION ]]; then PARTITION=none; fi
cd ..
./run_job.sh -t 15 -m 16 -n "reach+aut-heur" -p $PARTITION -r "-s BestFS --ltl-por reach --ltl-heur aut" verifypn-linux64 mcc2021
cd experiments
