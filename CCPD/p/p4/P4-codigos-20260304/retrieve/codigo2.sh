#!/bin/bash
SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)
export PRACTICA="P5"
export INFRASTRUCTURE="MR"
source ${SCRIPTPATH}/../vars.sh

experiment=${1}

DECIMAL_SEP="."

function parse_data {
  cat ${RESULTS_DIR}/* | grep "DATA|" | sed "s/DATA|//" > 1.csv
  cat ${RESULTS_DIR}/* | grep "User time" | cut -d " " -f 4 > 2.csv
  cat ${RESULTS_DIR}/* | grep "System time" | cut -d " " -f 4  > 3.csv

  echo "${RESULTS_LABEL}"
  echo "______________________________________________________"
  paste -d ';' 1.csv 2.csv 3.csv | sed "s/\./${DECIMAL_SEP}/g"
  echo "______________________________________________________"
  rm 1.csv 2.csv 3.csv
}

if [ ${experiment} == "amdahl" ]
then
  echo "Retrieving results of amdahl remote experiments"
	
  rm -Rf results/amdahl
  mkdir -p results/amdahl

  echo "Retrieving amdahl results from MR"
  echo "------------------------------------"
  scp -P $PORT alumno@$IP_PUBLIC:$MY_DIR/results_amdahl/* results/amdahl/
  echo "------------------------------------"

  RESULTS_DIR=results/amdahl
  RESULTS_LABEL="AMDAHL RESULTS"
  parse_data

elif [ ${experiment} == "gustafson" ]
then
  echo "Retrieving results of gustafson remote experiments"
  
  rm -Rf results/gustafson/gen
  mkdir -p results/gustafson/gen

  echo "Retrieving gustafson results from MR"
  echo "------------------------------------"
  scp -P $PORT alumno@$IP_PUBLIC:$MY_DIR/results_gustafson/gen/* results/gustafson/gen/
  echo "------------------------------------"

  RESULTS_DIR=results/gustafson/gen
  RESULTS_LABEL="GUSTAFSON RESULTS -- GEN"
  parse_data

else
  echo "You must choose to execute either 'amdahl' or 'gustafson'"
  exit 1
fi



