#!/bin/bash
SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)
export PRACTICA="P5"
export INFRASTRUCTURE="MR"
source ${SCRIPTPATH}/../vars.sh

experiment=${1}

if [ "${experiment}" == "amdahl" ]
then
  echo "Executing amdahl remote experiments"
elif [ "${experiment}" == "gustafson" ]
then
  echo "Executing gustafson remote experiments"
else
  echo "You must choose to execute either 'amdahl' or 'gustafson'"
  exit 1
fi


ssh alumno@${IP_PUBLIC} -p ${PORT} "mkdir -p $MY_DIR"
ssh alumno@${IP_PUBLIC} -p ${PORT} "touch $MY_DIR"
ssh alumno@${IP_PUBLIC} -p ${PORT} "touch /home/alumno/${USERNAME}"
scp -P ${PORT} ${SCRIPTPATH}/${experiment}_script.sh alumno@${IP_PUBLIC}:${MY_DIR}
scp -P ${PORT} ${SCRIPTPATH}/../generate_data.py alumno@${IP_PUBLIC}:${MY_DIR}
scp -P ${PORT} ${SCRIPTPATH}/../codigo2.py alumno@${IP_PUBLIC}:${MY_DIR}
JOB_ID=$(ssh alumno@$IP_PUBLIC -p ${PORT} "\
  cd $MY_DIR && \
  export failsafe=\"deactivated\" && \
  tsp -L ${USERNAME} bash -c 'timeout ${TIMEOUT} bash ${experiment}_script.sh'")

echo "Tu trabajo ha sido encolado con el ID '${JOB_ID}', puedes usarlo para comprobar su estado, su salida, o para pararlo"

