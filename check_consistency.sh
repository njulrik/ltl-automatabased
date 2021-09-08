#!/bin/bash

#Usage model_folder binaryA binaryB {LTL,CTL}
#set -x

if [[ $# -lt 3 ]]
then
    echo "Usage: MODEL_FOLDER BINARY-NAME BINARY-NAME [CATEGORY]"
    echo 
    echo "Compares the contents of output/MODEL_FOLDER for each given binary name"
    echo " in the specified category. If CATEGORY is omitted, default to LTL"
    exit 0
elif [[ $# -eq 3 ]]
then
    CATEGORY=LTL
else 
    CATEGORY=$4
fi

for p in "$CATEGORY"{Cardinality,Fireability} ; do

    for f in $2 $3 ; do 
	    find output/$1/$f -name "*.$p" -exec grep FORMULA {} +  | grep -oP '(?<=FORMULA ).*(?= TECHNIQUES)' | sort | uniq > answers/$1.$f.$p
	    #grep FROM output/$1/$f/*.$p* | grep -oP '(?<=FORMULA ).*(?= TECHNIQUES)' | sort | uniq > answers/$1.$f.$p
    done 

    LEFT=$(comm -13 answers/$1.${2}.$p answers/$1.${3}.$p | grep -oP '.*(?= (TRUE|FALSE))')
    RIGHT=$(comm -23 answers/$1.${2}.$p answers/$1.${3}.$p | grep -oP '.*(?= (TRUE|FALSE))')
    echo "DIFFERENCES IN $p : "

    comm -12 <(echo "$LEFT" | sort) <(echo "$RIGHT" | sort)
    C1=$(cat answers/$1.${2}.$p | wc -l)
    C2=$(cat answers/$1.${3}.$p | wc -l)
    echo "$1.${2}.$p -> $C1"
    echo "$1.${3}.$p -> $C2" 
done
