export PRACTICA="P6"
export INFRASTRUCTURE="MR"
source vars.sh
export CODE="codigo1_balanceo.py"

# Because a file has to be sent before execution, the directory has to be created now
ssh alumno@$IP_PUBLIC -p ${PORT} "mkdir -p $MY_DIR"
scp -P ${PORT} auxiliar.py alumno@$IP_PUBLIC:$MY_DIR
###

bash scripts/execute.sh

