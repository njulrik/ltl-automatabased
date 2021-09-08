#!/bin/bash

cd ..
./run_job.sh -t 15 -m 16 -n "torsten+heur" -r "-s BestFS --ltl-heur aut --ltl-por automaton" reach-stub-new@263 mcc2021
cd experiments
