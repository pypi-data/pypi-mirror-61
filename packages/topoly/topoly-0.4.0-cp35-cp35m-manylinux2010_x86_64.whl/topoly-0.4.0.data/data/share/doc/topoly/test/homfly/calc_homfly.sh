#!/usr/bin/env bash

HOMFLY_EXE=$1
POLY_EXE=$2
NCUC_EXE=$3
KNOT_OUT=$4

for file in ../data/lasso_*.xyz
do
    $HOMFLY_EXE -p 1 -c 0 -i $file
    $POLY_EXE EMCode.txt
done
$NCUC_EXE LMKNOT.txt > $KNOT_OUT 
rm LMKNOT.txt
rm EMCode.txt
