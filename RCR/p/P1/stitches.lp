%Miembros:
%    - Xoel Sánchez Dacoba
%    - Sebastián David Moreno Expósito
%Grupo de prácticas:
%    G1.1 - Lunes.
%Encoding type -> 0


row(0..N-1) :- size(N).%Generamos filas y columnas
col(0..N-1) :- size(N).

ady_cells(X,Y, X+1,Y) :- region(X,Y,R1), region(X+1,Y,R2), row(X), row(X+1).% Aqui de define la adyacencia, para simplificar, se define que dos celdas son adyacentes si estan una al lado de la otra, ya sea horizontal o verticalmente, y pertenecen a regiones diferentes
ady_cells(X,Y, X,Y+1) :- region(X,Y,R1), region(X,Y+1,R2), col(Y), col(Y+1).

{ stitch(X,Y, X1,Y1) } :- ady_cells(X,Y, X1,Y1), region(X,Y,R1), region(X1,Y1,R2), R1 != R2.%Regla que define que se puede colocar una puntada entre dos celdas adyacentes si pertenecen a regiones diferentes

hole(X,Y)   :- stitch(X,Y, X1,Y1).%Definimos que una celda tiene un agujero si tiene una puntada
hole(X1,Y1) :- stitch(X,Y, X1,Y1).%Lo mismo, pero para la otra celda de la puntada, ya que una puntada afecta(genera agujero) a dos celdas

:- hole(X,Y), #count{ X1,Y1 : stitch(X,Y, X1,Y1) ; X1,Y1 : stitch(X1,Y1, X,Y) } > 1.%Regla que define que no puede haber mas de una puntada en una celda

connected_regions(R1, R2) :- ady_cells(X,Y, X1,Y1), region(X,Y,R1), region(X1,Y1,R2), R1 < R2.%Definimos que dos regiones estan conectadas si hay una puntada entre ellas
connected_regions(R1, R2) :- ady_cells(X,Y, X1,Y1), region(X,Y,R2), region(X1,Y1,R1), R1 < R2.

:- connected_regions(R1, R2), m(M), #count{ X,Y,X1,Y1 : stitch(X,Y,X1,Y1), region(X,Y,R1), region(X1,Y1,R2) ;
X,Y,X1,Y1 : stitch(X,Y,X1,Y1), region(X,Y,R2), region(X1,Y1,R1) } != M.%Esta regla es más compleja, pero lo que hace es sencillo
% elimina las soluciones en las que el número de puntadas entre dos regiones conectadas no es igual a M

:- col(Y), t_c(Y, T), #count{ X : hole(X,Y) } != T.%Aqui eliminamos las soluciones que no cumplen con el total de agujeros por columna
:- row(X), t_r(X, T), #count{ Y : hole(X,Y) } != T.%Aqui las de las filas