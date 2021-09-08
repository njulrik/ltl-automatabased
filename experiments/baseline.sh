#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "baseline" -r "-s DFS --ltl-por none" reach-stub-new@263 mcc2021
cd experiments
