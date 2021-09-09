#!/bin/bash

set +x

if [[ -z $PARTITION ]]; then PARTITION=none; fi

cd experiments
for f in $(ls); do
    ./$f
done
cd ..
