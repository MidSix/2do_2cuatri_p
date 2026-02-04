
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****488Z
*****510Q
*****754R
*****079T

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Error al ejecutar la funcion: DimensionMismatch: tried to assign 2×2 array to 3×3×1 destination


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Error al ejecutar la funcion: MethodError: no method matching trainClassDoME(::Matrix{Float64}, ::Vector{String}, ::Int64)
The function `trainClassDoME` exists, but no method is defined for this combination of argument types.

Closest candidates are:
  trainClassDoME(!Matched::Tuple{AbstractMatrix{<:Real}, AbstractVector{Bool}}, !Matched::AbstractMatrix{<:Real}, ::Int64)
   @ Main <corrector>:818
  trainClassDoME(!Matched::Tuple{AbstractMatrix{<:Real}, AbstractVector}, !Matched::AbstractMatrix{<:Real}, ::Int64)
   @ Main <corrector>:820
  trainClassDoME(!Matched::Tuple{AbstractMatrix{<:Real}, AbstractMatrix{Bool}}, !Matched::AbstractMatrix{<:Real}, ::Int64)
   @ Main <corrector>:819



   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 0.75


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****541A
*****998T
*****886D
*****738E

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****959Y
*****940Y

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Error al ejecutar la funcion con parametros de tipo (targets::AbstractArray{<:Any,1}, k::Int64): DimensionMismatch: array could not be broadcast to match destination

   ANNCrossValidation:
      Valor promedio de la metrica precisión incorrecto al entrenar la RNA con conjunto de validación
      Desviacion tipica de la metrica precisión incorrecta al entrenar la RNA con conjunto de validación
      Valor promedio de la metrica tasa de error incorrecto al entrenar la RNA con conjunto de validación
      Desviacion tipica de la metrica tasa de error incorrecta al entrenar la RNA con conjunto de validación
      Valor promedio de la metrica sensibilidad incorrecto al entrenar la RNA con conjunto de validación
      Desviacion tipica de la metrica sensibilidad incorrecta al entrenar la RNA con conjunto de validación
      Valor promedio de la metrica especificidad incorrecto al entrenar la RNA con conjunto de validación
      Desviacion tipica de la metrica especificidad incorrecta al entrenar la RNA con conjunto de validación
      Valor promedio de la metrica VPP incorrecto al entrenar la RNA con conjunto de validación
      Desviacion tipica de la metrica VPP incorrecta al entrenar la RNA con conjunto de validación
      Valor promedio de la metrica VPN incorrecto al entrenar la RNA con conjunto de validación
      Desviacion tipica de la metrica VPN incorrecta al entrenar la RNA con conjunto de validación
      Valor promedio de la metrica F1 incorrecto al entrenar la RNA con conjunto de validación
      Desviacion tipica de la metrica F1 incorrecta al entrenar la RNA con conjunto de validación
      La matriz de confusión promedia en test obtenida al entrenar la RNA con conjunto de validación tiene valores incorrectos
      Valor promedio de la metrica precisión incorrecto al entrenar la RNA sin conjunto de validación
      Desviacion tipica de la metrica precisión incorrecta al entrenar la RNA sin conjunto de validación
      Valor promedio de la metrica tasa de error incorrecto al entrenar la RNA sin conjunto de validación
      Desviacion tipica de la metrica tasa de error incorrecta al entrenar la RNA sin conjunto de validación
      Valor promedio de la metrica sensibilidad incorrecto al entrenar la RNA sin conjunto de validación
      Desviacion tipica de la metrica sensibilidad incorrecta al entrenar la RNA sin conjunto de validación
      Valor promedio de la metrica especificidad incorrecto al entrenar la RNA sin conjunto de validación
      Desviacion tipica de la metrica especificidad incorrecta al entrenar la RNA sin conjunto de validación
      Valor promedio de la metrica VPP incorrecto al entrenar la RNA sin conjunto de validación
      Desviacion tipica de la metrica VPP incorrecta al entrenar la RNA sin conjunto de validación
      Valor promedio de la metrica VPN incorrecto al entrenar la RNA sin conjunto de validación
      Desviacion tipica de la metrica VPN incorrecta al entrenar la RNA sin conjunto de validación
      Valor promedio de la metrica F1 incorrecto al entrenar la RNA sin conjunto de validación
      Desviacion tipica de la metrica F1 incorrecta al entrenar la RNA sin conjunto de validación
      La matriz de confusión promedia en test obtenida al entrenar la RNA sin conjunto de validación tiene valores incorrectos


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Error al ejecutar la funcion: MethodError: no method matching fit!(::Nothing)
The function `fit!` exists, but no method is defined for this combination of argument types.

Closest candidates are:
  fit!(!Matched::MLJBase.Source; args...)
   @ MLJBase C:\Users\dani\.julia\packages\MLJBase\7nGJF\src\composition\learning_networks\nodes.jl:261
  fit!(!Matched::Machine; kwargs...)
   @ MLJBase C:\Users\dani\.julia\packages\MLJBase\7nGJF\src\machines.jl:786
  fit!(!Matched::Node; acceleration, kwargs...)
   @ MLJBase C:\Users\dani\.julia\packages\MLJBase\7nGJF\src\composition\learning_networks\nodes.jl:217
  ...



   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 0.65


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****120M
*****997D
*****416A
*****241M

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****950K
*****088V
*****553J
*****048A

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****689E
*****940P
*****3584

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      La salida de la función de parametros (trainingDataset::Tuple{AbstractArray{<:Real,2}, AbstractArray{Bool,1}}, testInputs::AbstractArray{<:Real,2}, maximumNodes::Int) no es de tipo AbstractVector{Float64}


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Error al ejecutar la funcion: UndefVarError: `fit!` not defined in `Main`
Hint: It looks like two or more modules export different bindings with this name, resulting in ambiguity. Try explicitly importing it from a particular module, or qualifying the name with the module it should come from.
Hint: a global variable of this name may be made accessible by importing StatsBase in the current active module Main
Hint: a global variable of this name may be made accessible by importing MLJBase in the current active module Main
Hint: a global variable of this name also exists in MLJ.
Hint: a global variable of this name may be made accessible by importing ScikitLearnBase in the current active module Main
Hint: a global variable of this name also exists in LIBSVM.
Hint: a global variable of this name may be made accessible by importing DecisionTree in the current active module Main


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 0.75


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****153F
*****614P
*****622V
*****394Z

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****184X
*****041N
*****688H

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****321D
*****616E
*****254T
*****126Y

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****978N
*****065H
*****893Y
*****480R

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****700Q
*****422X
*****318R

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****702Y
*****911L
*****045R
*****672Z

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****263M
*****198X
*****738R
*****358L

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****270L
*****953J
*****104V

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Error al ejecutar la funcion de parametros (trainingDataset::Tuple{AbstractArray{<:Real,2}, AbstractArray{Bool,2}}, testInputs::AbstractArray{<:Real,2}, maximumNodes::Int) al pasar como salidas deseadas una matriz de una columna (dos clases): StackOverflowError:


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Error al ejecutar la funcion con parametros de tipo (N::Int64, k::Int64): AssertionError: k >= 10
      Error al ejecutar la funcion con parametros de tipo (targets::AbstractArray{Bool,1}, k::Int64): AssertionError: k >= 10
      Error al ejecutar la funcion con parametros de tipo (targets::AbstractArray{Bool,2}, k::Int64): AssertionError: k >= 10
      Error al ejecutar la funcion con parametros de tipo (targets::AbstractArray{<:Any,1}, k::Int64): AssertionError: k >= 10

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 0.9


-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------

Autores:
*****519L
*****091R
*****294S
*****124P

   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 4

   confusionMatrix (clasificacion binaria):
      Nota: 0.2

   confusionMatrix (clasificacion multiclase):
      Nota: 0.2

   trainClassDoME:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 5

   crossvalidation:
      Nota: 0.1

   ANNCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Ejercicio 6

   modelCrossValidation:
      Nota: 0.25


   -------------------------------------------------------------------------------------------------------------------------
   Nota del archivo entregado: 1.25

