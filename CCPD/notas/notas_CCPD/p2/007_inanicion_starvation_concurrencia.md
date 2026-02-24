# 007_inanicion_starvation_concurrencia.md

**Página de referencia en `EnunciadoP2.pdf`:** 14 (Sección 3.4: "Inanición software", Tarea 11), 15 (Tarea 11 y `codigo4-ProdConsInanition.py`) y 16 (Figura 13).

## Inanición (Starvation) en Sistemas Concurrentes

La **inanición** (starvation) es un problema en la programación concurrente donde un proceso o hilo es repetidamente denegado el acceso a un recurso necesario por parte de otros procesos o hilos, a pesar de que el recurso se vuelve disponible. Esto ocurre cuando la programación (scheduling) de los recursos es injusta o cuando la lógica de acceso favorece constantemente a algunos hilos sobre otros.

A diferencia del **deadlock**, donde todos los hilos involucrados están bloqueados indefinidamente, en la inanición los hilos no están necesariamente bloqueados; simplemente no consiguen obtener los recursos que necesitan para progresar.

### Escenario de Inanición (`codigo4-ProdConsInanition.py`)

La Tarea 11 del `EnunciadoP2.pdf` propone un escenario para observar la inanición utilizando el `codigo4-ProdConsInanition.py`, que simula dos consumidores ("Fast consumer" y "Slow consumer") compitiendo por un único "comedor" (representado por un lock `item_ready`).

*   **`consumerFast()`:** Este consumidor intenta adquirir el lock (`item_ready.acquire()`) de forma voraz y sin espera si el lock no está disponible. Después de "comer" y liberar el lock, intenta adquirirlo de nuevo inmediatamente (`fast_notify("Going to queue to eat again")`).
*   **`consumerSlow()`:** Este consumidor es más "educado". Cuando intenta adquirir el lock (`item_ready.acquire(timeout=0.1)`) y descubre que no está disponible (debido al `timeout`), se retira temporalmente (`slow_notify("Someone is inside, going to make time")` y `time.sleep(1)`), permitiendo que otros hilos (el `consumerFast`) accedan al recurso. Después de liberar el lock, también toma un "paseo" (`time.sleep(1)`).

### ¿Cómo se Produce la Inanición?

Debido a la naturaleza "voraz" y persistente de `consumerFast`, y la disposición de `consumerSlow` a esperar y retirarse, el `consumerFast` adquiere el lock la vasta mayoría de las veces. El `consumerSlow` rara vez, o quizás nunca, consigue adquirir el lock, lo que le impide avanzar en su tarea de consumir ítems. Esto es inanición: el recurso (`item_ready`) está disponible (es liberado por `consumerFast`), pero `consumerSlow` no logra acceder a él porque `consumerFast` lo adquiere casi inmediatamente después de liberarlo.

La Figura 13 en la página 16 muestra la ejecución del `codigo4-ProdConsInanition.py`, donde se puede observar cómo el "Fast consumer" realiza múltiples operaciones de consumo mientras el "Slow consumer" apenas progresa o se queda esperando indefinidamente.

### Causas y Consecuencias

La inanición puede ser causada por:
*   **Programación (scheduling) injusta:** El planificador del sistema operativo favorece consistentemente a ciertos hilos.
*   **Prioridades de hilos:** Hilos de alta prioridad monopolizan los recursos, impidiendo que los de baja prioridad los obtengan.
*   **Algoritmos de acceso a recursos:** La lógica de acceso a recursos compartidos favorece de forma injusta a algunos hilos, como se ve en el ejemplo.

La inanición reduce la eficiencia del sistema, ya que los hilos "inanidos" no contribuyen al trabajo total y pueden consumir ciclos de CPU intentando repetidamente adquirir recursos sin éxito.
