# 002 - Práctica 1: Comandos Clave y Consideraciones en Contenedores (CCPD)

Este documento resume los comandos clave introducidos en la `Práctica 1: Gestión de recursos y repaso de programación` de Computación Concurrente, Paralela y Distribuida, junto con consideraciones importantes al ejecutarlos en entornos de contenedor Docker.

## 1. Resumen de la Práctica 1

La Práctica 1 introduce la gestión y el análisis de recursos en Linux, fundamental para comprender el rendimiento y el paralelismo. Revisa paradigmas de programación (imperativo y funcional) y enfatiza el uso de contenedores Docker para la ejecución de programas, siendo el entorno oficial para la resolución de dudas. Los objetivos incluyen la identificación de hardware, el análisis del consumo de recursos en tiempo real, la medición de tiempos de ejecución y el estudio del estilo de programación y la programación funcional en Python.

## 2. Comandos Clave y su Funcionamiento

Aquí se detallan los comandos principales que se utilizarán durante la práctica:

### 2.1. `cat /proc/cpuinfo`
*   **Descripción:** Identifica el procesador del sistema.
*   **Funcionamiento/Salida Esperada:** Muestra información detallada de la CPU, como el modelo (`model name`), número de núcleos, velocidad de reloj (`cpu MHz`), tamaño de caché, capacidades (flags) y posibles errores de hardware. Esencial para conocer el entorno de ejecución.
*   **Ejemplo de Ejecución:**
    ```bash
    cat /proc/cpuinfo
    ```

### 2.2. `cat /proc/meminfo`
*   **Descripción:** Muestra la memoria disponible en el sistema.
*   **Funcionamiento/Salida Esperada:** Presenta datos sobre la memoria total (`MemTotal`), libre (`MemFree`), disponible (`MemAvailable`), espacio de intercambio (swap) y estadísticas de caché, todo en KiB. Permite entender los recursos de memoria.
*   **Ejemplo de Ejecución:**
    ```bash
    cat /proc/meminfo
    ```

### 2.3. `lshw` (con `sudo`)
*   **Descripción:** Analiza los recursos de hardware reales del sistema nativo (fuera del contenedor) en Linux. Requiere permisos de superusuario.
*   **Funcionamiento/Salida Esperada:** Proporciona un listado exhaustivo de todos los componentes de hardware del equipo.
*   **Ejemplo de Ejecución:**
    ```bash
    sudo lshw
    ```

### 2.4. `atop`
*   **Descripción:** Monitor de sistema y procesos en tiempo real, útil para analizar el consumo de recursos y detectar anomalías.
*   **Funcionamiento/Salida Esperada:** Muestra una interfaz interactiva con información de CPU, memoria, disco y red, así como datos por proceso.
*   **Opciones Clave:**
    *   `i<segundos>`: Cambia el intervalo de refresco (ej. `i5`).
    *   `p`: Agrupa la información por tipo de proceso.
    *   `c`: Muestra información de procesos individualmente.
    *   `g`: Muestra información de recursos de procesos individuales.
    *   `a`: Alterna entre mostrar todos los procesos del sistema o solo los activos.
    *   `k <PID>`: Mata un proceso con el ID especificado.
    *   `q`: Sale de la aplicación.
*   **Ejemplo de Ejecución:**
    ```bash
    atop
    ```
    *   Para cambiar el intervalo a 5 segundos:
        ```bash
        atop -i 5
        ```
    *   Para matar un proceso (ej. PID 123):
        ```bash
        atop -k 123
        ```
*   **Nota:** Si la salida está incompleta, redimensionar la terminal puede ayudar.

### 2.5. `htop`
*   **Descripción:** Visor de procesos interactivo más simple y rápido que `atop`, también para monitorización en tiempo real.
*   **Funcionamiento/Salida Esperada:** Ofrece una vista interactiva y colorida de procesos, uso de CPU (por núcleo), memoria y swap.
*   **Ejemplo de Ejecución:**
    ```bash
    htop
    ```

### 2.6. `stress -c <num_cpus>`
*   **Descripción:** Estresa la CPU lanzando procesos que consumen ciclos de CPU.
*   **Funcionamiento/Salida Esperada:** Inicia `<num_cpus>` trabajadores que realizan cálculos intensivos, llevando la utilización de la CPU al máximo. Útil para observar el sistema bajo carga. Para detenerlo, usar `Ctrl + C`.
*   **Ejemplo:** `stress -c 2` (estresa con 2 trabajadores de CPU).
*   **Ejemplo de Ejecución:**
    ```bash
    stress -c 4
    ```
### 2.7. `stress -c <num_cpus> -t <segundos>`
*   **Descripción:** Igual que `stress -c`, pero limita el tiempo de ejecución.
*   **Funcionamiento/Salida Esperada:** Lanza `<num_cpus>` trabajadores de CPU durante `<segundos>` segundos para un estrés controlado.
*   **Ejemplo:** `stress -c 2 -t 5` (estresa con 2 trabajadores de CPU durante 5 segundos).
*   **Ejemplo de Ejecución:**
    ```bash
    stress -c 2 -t 10
    ```

### 2.8. `stress-ng --vm <num_workers> --vm-bytes <tamaño> --vm-keep --vm-populate`
*   **Descripción:** Herramienta avanzada para generar uso artificial de memoria.
*   **Funcionamiento/Salida Esperada:**
    *   `--vm <num_workers>`: Número de trabajadores de memoria virtual.
    *   `--vm-bytes <tamaño>`: Cantidad de memoria virtual a asignar (ej. `512M`).
    *   `--vm-keep`: Mantiene la memoria asignada.
    *   `--vm-populate`: Rellena la memoria asignada.
*   Se utiliza para probar la estabilidad del sistema bajo presión de memoria.
*   **Ejemplo de Ejecución:**
    ```bash
    stress-ng --vm 1 --vm-bytes 1G --vm-keep --vm-populate
    ```

### 2.9. `time <comando>`
*   **Descripción:** Mide el tiempo de ejecución de un comando o programa.
*   **Funcionamiento/Salida Esperada:** Ejecuta el `<comando>` y reporta tres métricas de tiempo:
    *   **`real` (tiempo de pared):** Tiempo total transcurrido.
    *   **`user` (tiempo de CPU de usuario):** Tiempo de CPU dedicado al código del usuario.
    *   **`sys` (tiempo de CPU de sistema):** Tiempo de CPU dedicado al código del kernel en nombre del proceso.
*   **Importante:** La suma `user + sys` no siempre es igual a `real`, ya que el proceso puede haber estado esperando (I/O, bloqueado, etc.).
*   **Ejemplo:** `time ls -lash -R /`
*   **Ejemplo de Ejecución:**
    ```bash
    time find / -name "*.txt"
    ```

### 2.10. `python3 <script.py>`
*   **Descripción:** Ejecuta un script de Python.
*   **Funcionamiento/Salida Esperada:** Ejecuta el código Python. Se usarán ejemplos para:
    *   **Medición de tiempos intra-código:** Con `time.time()` y `time.sleep()`.
    *   **Generación de números aleatorios:** Con `random.randint()`.
    *   **Formateo de cadenas:** Usando el método `.format()`.
    *   **Variables de configuración:** Variables en mayúsculas para controlar el comportamiento del código.
*   **Ejemplo de Ejecución:**
    ```bash
    python3 my_script.py
    ```

### **2.11.**  `ps`

- **Descripcion:** Devuelve los procesos que existen en el instante en que se ejecuta el comando. (se lee como **P**rocess **S**tatus)
- **Ejemplo de salida:**
```bash
ubuntu@ContenedorParalelismo --cpuset-cpus=0-7:~$ ps
  PID TTY          TIME CMD
   51 pts/3    00:00:00 bash
   68 pts/3    00:08:55 stress
   69 pts/3    00:08:55 stress
   78 pts/3    00:00:00 ps
```
"-" -> guion
### 2.12 `grep`

### **2.13.**  `pgrep p_name` == `ps -u user | grep p_name`

- **Descripción:** Devuelve el PID del proceso o procesos que tienen el mismo p_name, o sea, el mismo process name
- 
- Ejemplo de salida:
```bash
ubuntu@ContenedorParalelismo:~$ pgrep bash
7
25
106
ubuntu@ContenedorParalelismo:~$
#Esto quiere decir que hay 3 terminales bash abiertas en el contenedor que tienen esos respectivosd PID(Process ID)
```

## 3. Consideraciones al Ejecutar en Contenedores Docker

La ejecución de comandos dentro de un contenedor Docker introduce diferencias importantes respecto al sistema anfitrión (host):

*   **Aislamiento y Límites de Recursos:**
    *   **CPU:** `cat /proc/cpuinfo` puede mostrar la información del host, pero el número efectivo de núcleos disponibles para el contenedor estará limitado por la configuración de Docker. Comandos como `stress` operarán dentro de estos límites asignados.
    *   **Memoria:** `cat /proc/meminfo` mostrará la memoria asignada al contenedor. `stress-ng` estará limitado por la configuración de memoria del contenedor. Es crucial no asignar más de la mitad de la memoria disponible para evitar que el sistema anfitrión se ralentice o congele.
    *   **Sistema de Archivos:** El `root` filesystem del contenedor (`/`) está aislado del host. Los comandos de listado como `ls -lash -R /` mostrarán solo el contenido del contenedor.

*   **Información del Kernel:** `cat /proc/cpuinfo` y `cat /proc/meminfo` leen pseudo-archivos que reflejan la vista del kernel *para el contenedor*, no necesariamente el hardware físico del host si el runtime del contenedor abstrae o limita esa vista.

*   **Gestión de Procesos:** `atop` y `htop` solo mostrarán los procesos *dentro del contenedor*. Las señales `kill` enviadas desde el contenedor solo afectarán a procesos dentro del mismo.

*   **Permisos de Usuario:** Aunque se pueda ejecutar como `root` dentro del contenedor, estos privilegios no se extienden al sistema host.

*   **Reproducibilidad:** El uso de Docker busca la reproducibilidad. Esto significa que los resultados de los comandos *deberían* ser consistentes entre diferentes entornos si la imagen y la asignación de recursos de Docker son uniformes, pero siempre en el contexto aislado del contenedor.

En resumen, los resultados obtenidos en un contenedor Docker están siempre acotados a su entorno aislado y a los recursos que se le hayan asignado, no al sistema host subyacente.

### 3.1. Aclaración sobre Memoria en WSL y Contenedores Docker

Es crucial entender que cuando se ejecuta `cat /proc/meminfo` desde una instancia de **WSL (Windows Subsystem for Linux)** o dentro de un **contenedor Docker** (que en Windows suele ejecutarse sobre una VM de WSL 2), la información reportada sobre la memoria (`MemTotal`, `MemAvailable`, etc.) **no corresponde a la memoria RAM física total del equipo host (Windows)**.

En estos entornos:
*   **WSL:** `MemTotal` muestra la cantidad de RAM que Windows ha asignado a la máquina virtual de WSL. Esta asignación es dinámica y puede crecer a demanda hasta un límite predefinido (configurable, pero que por defecto suele ser un porcentaje de la RAM física del host).
*   **Contenedores Docker (en WSL 2):** `cat /proc/meminfo` dentro de un contenedor Docker generalmente refleja la memoria del kernel de la VM de WSL 2 que lo aloja, no la memoria RAM total de tu máquina Windows, ni necesariamente el límite de recursos específico asignado al contenedor. Para verificar los límites de RAM asignados a un contenedor y su uso real, es más preciso usar comandos como `docker stats <nombre_del_contenedor>` o inspeccionar los `cgroups` del contenedor (ej. `cat /sys/fs/cgroup/memory/memory.limit_in_bytes` dentro del contenedor).

Esta distinción es fundamental para evitar confusiones al comparar la memoria reportada en el entorno virtualizado con la RAM física instalada en el hardware.
