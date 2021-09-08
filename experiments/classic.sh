#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "classic" -r "-s DFS --ltl-por classic" reach-stub-new@263 mcc2021
cd experiments
