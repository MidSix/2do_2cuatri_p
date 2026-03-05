#!/bin/bash
SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)
export PRACTICA="P5"
export INFRASTRUCTURE="MR"
source ${SCRIPTPATH}/../vars.sh

export CODE="codigo1.py"
bash ${SCRIPTPATH}/../scripts/execute.sh

