#!/bin/bash

source vars.sh

for var in "$@"
do
  echo "Borrando ${var}"
  ssh alumno@${IP_PUBLIC} -p ${PORT} "tsp -r ${var}"
done


