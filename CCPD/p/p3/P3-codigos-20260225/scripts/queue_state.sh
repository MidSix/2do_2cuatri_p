#!/bin/bash

source vars.sh

echo "Consulting queue"
ssh alumno@${IP_PUBLIC} -p ${PORT} "tsp "

echo "Consulting queue with label (username) '${USERNAME}'"
ssh alumno@${IP_PUBLIC} -p ${PORT} "tsp | grep '${USERNAME}'"