#!/bin/bash

cd ..
./run_job.sh -t 15 -m 16 -n torsten -r "-s DFS --ltl-por automaton" reach-stub-new@263 mcc2021
cd experiments
