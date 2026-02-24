Hola. He leído los dos documentos que me has proporcionado. Aquí tienes la
  explicación para abordar el tercer apartado de la práctica, incluyendo la
  solución al "acertijo MU" y la discusión sobre el procedimiento de decisión.

  

  **Resumen del Problema (Ejercicio 3: Sistema MIU)**

  

  Recordemos las reglas del sistema MIU:

  

   * **Alfabeto:** {M, I, U}
   * **Axioma (único teorema inicial):** MI
   * **Reglas de Producción:**

       1. Si tienes xI, puedes obtener xIU (añadir U al final si acaba en I).
       2. Si tienes Mx, puedes obtener Mxx (duplicar la cadena después de la M).
       3. Si encuentras III en un teorema, puedes reemplazarlo por U.
       4. Si encuentras UU en un teorema, puedes eliminarlo.

  

  ---

  

  **1. El Acertijo MU: ¿Se puede producir la cadena** **MU****?**

  

  La respuesta corta es **no, no se puede**.

  

  La clave para resolver este acertijo no es intentar generar teoremas hasta
  encontrar MU (lo cual nunca ocurrirá), sino encontrar un **invariante**: una
  propiedad que es cierta para el axioma inicial y que se conserva después de
  aplicar cualquiera de las reglas.

  

  Analicemos el **número de letras 'I'** en los teoremas:

  

   1. **Axioma `MI`**: Empezamos con **1** letra 'I'.

   2. **Análisis de las reglas y su efecto en el número de 'I's**:
       * **Regla 1 (`xI` → `xIU`):** No cambia el número de 'I's.
       * **Regla 2 (`Mx` → `Mxx`):** Duplica el número de 'I's que hay en la cadena
         x. Si el número de 'I's era N, ahora será 2 * N.
       * **Regla 3 (`III` → `U`):** Reduce el número de 'I's en 3. Si era N, ahora
         será N - 3.
       * **Regla 4 (`UU` → `_`):** No cambia el número de 'I's.

  

  Ahora, pensemos en la cantidad de 'I's módulo 3:

  

   * El axioma MI tiene 1 'I'. 1 mod 3 = 1.
   * La **Regla 2** (duplicar) nunca producirá un número de 'I's que sea múltiplo de
     3.
       * Si partimos de un número N tal que N mod 3 = 1, el nuevo número 2N
         cumplirá 2N mod 3 = 2.
       * Si partimos de N tal que N mod 3 = 2, el nuevo número 2N cumplirá 4 mod
         3 = 1.
   * La **Regla 3** (restar 3) tampoco cambia el resultado del módulo 3. (N - 3) mod
     3 = N mod 3.
   * Las reglas 1 y 4 no afectan al número de 'I's.

  

  **Conclusión del invariante:**
  Partimos de un número de 'I's que no es múltiplo de 3 (es 1). Ninguna regla de
  producción puede generar un teorema cuyo número de 'I's sea un múltiplo de 3.

  

  El teorema que queremos obtener es **`MU`**. Este teorema tiene **0** letras 'I'. Como
  0 es un múltiplo de 3 (0 = 3 * 0), y hemos demostrado que el sistema nunca
  puede producir un teorema con un número de 'I's múltiplo de 3, podemos
  concluir con certeza que **`MU` no es un teorema del sistema MIU.**

  

  ---

  

  **2. El Procedimiento de Decisión para el Sistema MIU**

  

  La pregunta es: ¿existe un algoritmo (un "procedimiento de decisión") que,
  para _cualquier_ cadena dada, pueda determinar en un tiempo finito si es un
  teorema del sistema MIU o no?

  

  **Opinión y Análisis:**

  

  Un procedimiento de decisión debe terminar para **todas** las entradas posibles,
  tanto si la cadena es un teorema como si no lo es.

  

   1. **Búsqueda hacia adelante:** Podríamos intentar generar todos los teoremas
      posibles a partir de MI usando una búsqueda en anchura (BFS) para ser "no
      sesgados". Si en algún momento encontramos la cadena que buscamos, el
      algoritmo termina y devuelve "sí".

       * **El problema:** Si la cadena _no_ es un teorema (como MU), ¿cuándo paramos?
         Las reglas 1 y 2 alargan las cadenas, pero las reglas 3 y 4 las
         acortan. Esto significa que no podemos simplemente detener la búsqueda
         cuando los teoremas generados superen la longitud de la cadena
         objetivo, ya que una cadena más larga podría, teóricamente, reducirse
         más tarde. El proceso de búsqueda para una cadena que no es un teorema
         podría no terminar nunca.

  

   2. **Comparación con el sistema `mg~` (ejercicio 2):** En ese sistema, las reglas
      solo alargan los teoremas. Por lo tanto, un procedimiento de decisión es
      trivial: generas todos los teoremas hasta que su longitud supere la de la
      cadena objetivo. Si no la has encontrado, nunca lo harás. El sistema mg~
      es **decidible**.

  

   3. **El sistema MIU:** La capacidad de acortar cadenas lo complica todo. Nos
      enfrenta a un problema fundamental de la computación muy relacionado con
      el **problema de la parada (Halting Problem)**. En general, los sistemas
      formales con este tipo de reglas (que pueden alargar y acortar cadenas sin
      un límite claro) suelen ser **indecidibles**.

  

  **Opinión final:**

  Mi opinión es que **no existe un procedimiento de decisión** para el sistema MIU.
  Implementar un programa que genere teoremas es posible (como se pide en la
  primera parte del ejercicio), pero no un algoritmo que garantice la parada
  para cadenas que no son teoremas. La justificación es que el espacio de
  búsqueda es infinito y no parece haber una cota superior para podar la
  búsqueda de manera efectiva, lo que sugiere que el sistema es indecidible.

  

  Para la práctica, la argumentación detallada de por qué es complejo y
  probablemente indecidible es la respuesta que se espera, más que una prueba
  formal de indecidibilidad, que es extremadamente compleja.

  

  Espero que esto te sea de gran ayuda para completar la práctica. ¡Mucho éxito