export IP_PUBLIC="193.144.50.38"
export USERNAME="SebastianDavidMorenoExposito"
export MY_DIR="/home/alumno/${USERNAME}/${PRACTICA}"

if [ -z "${INFRASTRUCTURE}" ]; then
  echo "Empty 'INFRASTRUCTURE' variable"
  echo "You can set it using the command 'export INFRASTRUCTURE=\"MR\"' if you want to run this job on the MR, or CR otherwise"
  exit 1
fi

if [ ${INFRASTRUCTURE} == 'MR' ]; then
  export PORT=5244
elif [ ${INFRASTRUCTURE} == 'CR' ]; then
  export PORT=5723
else
  echo "Incorrect Infrastructure, only MR and CR are allowed"
  exit 1
fi

export TIMEOUT=$(curl -s https://dante.dec.udc.es/PP/${INFRASTRUCTURE}/api/timeout)
if [ "${CODE}" ]; then
  echo "Timeout is '${TIMEOUT}'"
fi
