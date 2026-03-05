#!/bin/bash

if [ "${failsafe}" != "deactivated" ]
then
  echo "This script is not meant to be executed outside the MR"
  exit 1
fi

DATA_SIZE=7
MAX_N_PROC=32
RESULTS_DIR="results_gustafson"
N_PROC_LIST=($(seq 2 2 ${MAX_N_PROC}))

#echo "Generating data of size ${MAX_N_PROC}e${DATA_SIZE}"
#python3 generate_data.py ${MAX_N_PROC}e${DATA_SIZE}

rm -Rf ${RESULTS_DIR}
mkdir -p ${RESULTS_DIR}/gen 
x=10
for i in "vec"
do
	echo "Running ${x}sec_vec_gen at `date +%H:%M:%S`"
	/usr/bin/time -v  python3 codigo2.py ${i} seq 0 1e${DATA_SIZE} gen &> ${RESULTS_DIR}/gen/${x}sec_${i}_gen.txt
	((x=x+1))
	for j in "${N_PROC_LIST[@]}";
	do
	  echo "Running ${x}par_${j}_${i}_gen at `date +%H:%M:%S`"
	  /usr/bin/time -v  python3 codigo2.py ${i} par ${j} ${j}e${DATA_SIZE} gen &> ${RESULTS_DIR}/gen/${x}par_${j}_${i}_gen.txt
	  ((x=x+1))
	done
done


#rm a.txt ax.txt b.txt bx.txt

