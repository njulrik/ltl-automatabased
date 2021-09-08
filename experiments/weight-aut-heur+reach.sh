#!/bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "weight-aut-heur+reach" -r "-s BestFS --ltl-heur aut --ltl-por reach" reach-stub-new@268 mcc2021
cd experiments
