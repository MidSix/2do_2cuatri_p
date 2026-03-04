**Descripción:** Es un problema de matemáticas y ajedrez que busca poder colocar n reinas en un tablero nxn de ajedrez tal que ninguna de esas n reinas se ataquen entre si.

- Toda reina se identifica en el tablero con un par ordenado (fila, columna)
### Constraints:
- NO puede haber 2 reinas que tengan el mismo par ordenado(Eso implicaría tener 2 reinas en una misma casilla, no tiene sentido)
- NO puede haber 2 reinas cuya primera coordenada sea la misma, es decir, NO pueden estar en la misma fila
- NO puede haber 2 reinas cuya segunda coordenada sea la misma, es decir, NO pueden estar en la misma columna
- NO puede ser que la diferencia entre la primera coordenada y  la segunda(entre el numero de filas y numero de columnas) sea la misma, en ese caso estarían en la misma diagonal. Diagonal principal o sus paralelas 
- NO puede ser que el resultado "n" de la suma de ambas coordenadas de una reina se repita, pues eso implicaría que están en la misma diagonal. La diagonal secundaria o sus paralelas. 