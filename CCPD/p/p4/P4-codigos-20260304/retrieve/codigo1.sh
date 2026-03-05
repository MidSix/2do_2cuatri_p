#!/bin/bash
SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)
export PRACTICA="P5"
export INFRASTRUCTURE="MR"
source ${SCRIPTPATH}/../vars.sh

mkdir -p results/codigo1

echo "Retrieving codigo1 results"
scp -P $PORT alumno@$IP_PUBLIC:$MY_DIR/results_codigo1/* results/codigo1/

