if [ -z "$IP_PUBLIC" ] || [ -z "$PORT" ] || [ -z "$USERNAME" ] || [ -z "$MY_DIR" ] || [ -z "$CODE" ]
then
      echo "Some variable is not set, can't execute:"
      echo "IP_PUBLIC -> $IP_PUBLIC"
      echo "PORT -> $PORT"
      echo "USERNAME -> $USERNAME"
      echo "MY_DIR -> $MY_DIR"
      echo "CODE -> $CODE"
      echo "Remember that this script is not meant to be executed directly"
      exit 1
fi

ssh alumno@${IP_PUBLIC} -p ${PORT} "mkdir -p $MY_DIR"
ssh alumno@${IP_PUBLIC} -p ${PORT} "touch $MY_DIR"
ssh alumno@${IP_PUBLIC} -p ${PORT} "touch /home/alumno/${USERNAME}"
scp -P ${PORT} ${CODE} alumno@${IP_PUBLIC}:${MY_DIR}
JOB_ID=$(ssh alumno@$IP_PUBLIC -p ${PORT} "\
  cd $MY_DIR && \
  tsp -L ${USERNAME} bash -c 'timeout ${TIMEOUT} python3 -u ${CODE} ${CODEARGS}'")

if [ $? == 0 ]
then
	echo "Tu trabajo ha sido encolado con el ID '${JOB_ID}', puedes usarlo para comprobar su estado, su salida, o para pararlo"
else
	echo "Hubo algún problema enviando tu trabajo para la ejecución remota, comprueba si hay errores en la salida y si ${INFRASTRUCTURE} está disponible"
fi
