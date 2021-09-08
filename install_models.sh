#!/bin/bash


mkdir -p mcc2021

if [[ ! -e mcc2021 ]]
then
    echo -n "Model directory mcc2021 already present. Proceed anyway? [y/N] "
    read -n 1 ans
    case $ans in
        y) ;;
        *) exit 0 ;;
    esac
fi

if [[ ! -e INPUTS-2021.tar.gz ]]
then
    echo "INPUTS-2021.tar.gz not found in $(pwd). Download from MCC'21 website? [Y/n] "
    read -n 1 ans
    case $ans in
        n)
            exit 0
            ;;
        *)
            wget https://mcc.lip6.fr/archives/INPUTS-2021.tar.gz
            ;;
    esac

fi

set -x

tar -xzf INPUTS-2021.tar.gz
for f in $(ls INPUTS-2021 | grep PT); do
    tar -xzf INPUTS-2021/$f -C mcc2021
done

rm INPUTS-2021.tar.gz
rm -rf INPUTS-2021
