#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -n "reach+aut-heur" -r "-s BestFS --ltl-por reach --ltl-heur aut" reach-stub-new@263 mcc2021
cd experiments
