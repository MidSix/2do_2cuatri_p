export PRACTICA="P3"
export INFRASTRUCTURE="MR"
source vars.sh

mkdir -p true_parallelism_remote
scp -P $PORT alumno@$IP_PUBLIC:$MY_DIR/true_parallelism/*.png true_parallelism_remote/

