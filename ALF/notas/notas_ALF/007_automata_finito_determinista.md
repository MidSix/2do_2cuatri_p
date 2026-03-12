 ![[Pasted image 20260312083347.png]]
 Para que un autómata sea un AFD (Autómata Finito Determinista), tiene que cumplir la
  "regla de la existencia y la unicidad" para cada símbolo del alfabeto:

   1. Teoría Práctica: Desde cada estado, debe salir exactamente una flecha por cada letra
      del alfabeto. Ni más, ni menos.
   2. El Alfabeto ($\Sigma$): En este ejemplo, el alfabeto es $\{a, b\}$.
> Por eso en ese ejemplo el automata NO es determinista.

![[Pasted image 20260312083452.png]]

> Tampoco es determinista porque debe salir exactamente una flecha con cada símbolo del alfabeto, pero en ese caso el estado q2 salen 3 flechas para solo 2 símbolos que tiene el alfabeto, eso implica que, al menos, un símbolo se repitió y eso no puede ser, deja de ser función si eso ocurre, por eso TAMPOCO es determinista.

- En el primero faltan flechas y en el segundo sobran, **no pueden faltar ni sobrar** tienen que haber las justas.

### Aceptación de una cadena:
- Una cadena es aceptada(procesada correctamente) por un automata, si y solo si empezando en el estado final, es capaz de procesar todos y cada uno de los símbolos de la cadena. Y "procesar" significa que desde el estado final somos capaces de llegar al estado de aceptación(final)
  3. La Regla de Oro para "Contiene"
  No te compliques la vida con los símbolos + o con intentar adivinar el orden. En los
  exámenes de ALF, "contiene" se traduce siempre como:

  [LO QUE SEA] + [LO QUE ME PIDEN] + [LO QUE SEA]


  Y "[LO QUE SEA]" en el alfabeto $\{a, b\}$ se escribe siempre como: $(a \cup b)^*$ (o
  también $(a | b)^$ o $(a+b)^$, según como lo escriba tu profesor).
