
 Para ello necesitas guardar una clave de acceso en el contenedor. Es decir, una llave ssh. Una llave que te permita acceder al shell de del servidor(MR)

- bash deploy-keys.sh -> Con esto guardamos la clave que se encuentra en el archivo deploy-keys.sh

ssh alumno@dante.dec.udc.es -p 5244 "echo 'I am on the machine named -->'; hostname; exit"