#!/bin/bash

source vars.sh

ssh alumno@${IP_PUBLIC} -p ${PORT} "tsp -i $1"
