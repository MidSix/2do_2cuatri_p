#!/bin/bash

source vars.sh

if [ -z "$1" ]
then
      echo "Tienes que indicar un id de trabajo inicial"
      exit
fi


if [ -z "$2" ]
then
      echo "Tienes que indicar un id de trabajo final"
      exit
fi

for var in $(seq $1 $2)
do
  echo "Borrando ${var}"
  ssh alumno@${IP_PUBLIC} -p ${PORT} "tsp -r ${var}"
done


