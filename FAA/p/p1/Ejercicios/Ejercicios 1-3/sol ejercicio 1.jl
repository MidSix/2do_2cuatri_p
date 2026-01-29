
    # Cargamos el dataset
    dataset = readdlm("iris.data",',');

    # Preparamos las entradas
    inputs = dataset[:,1:4];
    # Con cualquiera de estas 3 maneras podemos convertir la matriz de entradas de tipo Array{Any,2} en Array{Float32,2}, si los valores son numéricos:
    inputs = Float32.(inputs);
    inputs = convert(Array{Float32,2},inputs);
    inputs = [Float32(x) for x in inputs];
    println("Tamaño de la matriz de entradas: ", size(inputs,1), "x", size(inputs,2), " de tipo ", typeof(inputs));

    # Preparamos las salidas deseadas codificándolas puesto que son categóricas
    targets = dataset[:,5];
    println("Longitud del vector de salidas deseadas antes de codificar: ", length(targets), " de tipo ", typeof(targets));
    classes = unique(targets);
    numClasses = length(classes);
    if numClasses<=2
        # Si solo hay dos clases, se genera una matriz con una columna
        targets = reshape(targets.==classes[1], :, 1);
    else
        # Si hay mas de dos clases se genera una matriz con una columna por clase
        # Cualquiera de estos dos tipos (Array{Bool,2} o BitArray{2}) vale perfectamente
        # oneHot = Array{Bool,2}(undef, size(targets,1), numClasses);
        # oneHot =   BitArray{2}(undef, size(targets,1), numClasses);
        # for numClass = 1:numClasses
        #     oneHot[:,numClass] .= (targets.==classes[numClass]);
        # end;
        # Una forma de hacerlo sin bucles sería la siguiente:
        oneHot = convert(BitArray{2}, hcat([instance.==classes for instance in targets]...)');
        targets = oneHot;
    end;
    println("Tamaño de la matriz de salidas deseadas despues de codificar: ", size(targets,1), "x", size(targets,2), " de tipo ", typeof(targets));

    # Comprobamos que ambas matrices tienen el mismo número de filas
    @assert (size(inputs,1)==size(targets,1)) "Las matrices de entradas y salidas deseadas no tienen el mismo numero de filas"


    # Realizamos la normalizacion, de un tipo u otro. Por ejemplo, mediante maximo y minimo:
    # Primero calculamos los valores de normalizacion
    normalizationParameters = (minimum(inputs, dims=1), maximum(inputs, dims=1));
    # Despues los leemos de esa tupla
    minValues = normalizationParameters[1];
    maxValues = normalizationParameters[2];
    # En realidad, no es necesario crear la tupla con los parámetros de normalización, se podrían calcular directamente los valores máximo y mínimo sin almacenarlos en una tupla
    #  Esto se hace así para que, al tenerlo como una tupla, sea más sencillo pasarla a una función, como exige el ejercicio siguiente
    # Finalmente, los aplicamos
    inputs .-= minValues;
    inputs ./= (maxValues .- minValues);
    # Si hay algun atributo en el que todos los valores son iguales, se pone a 0
    inputs[:, vec(minValues.==maxValues)] .= 0;



    # Dejamos aqui indicado como se haria para normalizar mediante media y desviacion tipica
    # normalizationParameters = (mean(inputs, dims=1), std(inputs, dims=1));
    # avgValues = normalizationParameters[1];
    # stdValues = normalizationParameters[2];
    # inputs .-= avgValues;
    # inputs ./= stdValues;
    # # Si hay algun atributo en el que todos los valores son iguales, se pone a 0
    # inputs[:, vec(stdValues.==0)] .= 0;
