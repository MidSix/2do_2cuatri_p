#!/bin/bash

if [ "${failsafe}" != "deactivated" ]
then
  echo "This script is not meant to be executed outside the MR"
  exit 1
fi

DATA_SIZE=1e7
MAX_N_PROC=32
RESULTS_DIR="results_amdahl"

echo "Generating data of size ${DATA_SIZE}"
python3 generate_data.py ${DATA_SIZE}
N_PROC_LIST=(2 4 8 12 16 20 24 28 32)

rm -Rf ${RESULTS_DIR}
mkdir -p ${RESULTS_DIR}
x=10
for i in "vec" "list"
do
  echo "Running ${x}sec_${i}_file"
  /usr/bin/time -v  python3 codigo2.py ${i} seq 0 ${DATA_SIZE} file &> ${RESULTS_DIR}/${x}sec_${i}_file.txt
  ((x=x+1))
  for j in "${N_PROC_LIST[@]}";
  do
    echo "Running ${x}par_${j}_${i}_file"
    /usr/bin/time -v  python3 codigo2.py ${i} par ${j} ${DATA_SIZE} file &> ${RESULTS_DIR}/${x}par_${j}_${i}_file.txt
    ((x=x+1))
  done
done

#for i in "vec" "list"
#do
  #echo "Running ${x}sec_${i}_gen"
  #/usr/bin/time -v  python3 codigo2.py ${i} seq 0 ${DATA_SIZE} gen  &> ${RESULTS_DIR}/${x}sec_${i}_gen.txt
  #((x=x+1))
  #for j in "${N_PROC_LIST[@]}";
  #do
    #echo "Running ${x}par_${j}_${i}_gen"
    #/usr/bin/time -v  python3 codigo2.py ${i} par ${j} ${DATA_SIZE} gen &> ${RESULTS_DIR}/${x}par_${j}_${i}_gen.txt
    #((x=x+1))
  #done
#done

rm a.txt ax.txt b.txt bx.txt

