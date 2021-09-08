#!/usr/bin/env python3

max_time = 900
t_lower_bound = 30

baseline = "Baseline (no POR)"
classic = "Classic POR"
reach = "Automata-driven POR"
mixed = "Mixed"
torsten = "Liebke POR"

baseline_heur = "Baseline (heuristic)"
classic_heur = "Classic HPOR"
reach_heur = "Automata-driven HPOR"
torsten_heur = "Liebke HPOR"

firecount = "Fire Count"
distance = "Distance"
automaton = "State-based Heuristic"
weight_aut = "Weighted Automaton"
weight_aut_short = "Weight-aut"
aut_fc = "Automaton + Fire Count"
weightaut_fc = "Weight-aut + Fire Count"


dist_reach = "Distance + Reach"
aut_reach = "State-based Combination"
aut_mixed = "Automaton + Mixed"
autfc_mixed = "Aut./F. Count + Mixed"
weightfc_mixed = "Weight-aut/Fire count + Mixed"

dist_heur = "Distance Heuristic"
reach_stub = "Reachability Stubborn"
aut_heur = "Automaton Heuristic"
