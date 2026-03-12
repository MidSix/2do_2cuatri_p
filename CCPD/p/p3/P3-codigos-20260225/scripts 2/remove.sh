#!/bin/bash

source vars.sh

if [ -z "$1" ]
then
      echo "Tienes que indicar un id de trabajo, ASEGÚRATE QUE EL TRABAJO ES TUYO!"
      exit
fi


ssh alumno@${IP_PUBLIC} -p ${PORT} "tsp -r $1"

