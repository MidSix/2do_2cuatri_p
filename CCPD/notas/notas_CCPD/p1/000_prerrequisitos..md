- **Imagen: se descarga el dockerfile y se construye la imagen como cualquier otra**:

->`docker build -t <nombre_de_la_image> <path_del_dockerfile>`

- **Crear el contenedor a partir de una imagen**
docker run -d --name=ContenedorParalelismo -h ContenedorParalelismo --cpuset-cpus="0-4" --memory=16g -v C:\ai-career\900university\2do_curso\2do_cuatri\CCPD\p:/home/ubuntu/Practicas -p 4040:4040 cont-paralelismo:ubuntu24.04 /usr/bin/sleep infinity

