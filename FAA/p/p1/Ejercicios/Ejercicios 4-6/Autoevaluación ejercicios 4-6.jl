

# Archivo de pruebas para realizar autoevaluación de algunas funciones de los ejercicios

# Importamos el archivo con las soluciones a los ejercicios
include("soluciones.jl");
#   Cambiar "soluciones.jl" por el nombre del archivo que contenga las funciones desarrolladas

# Fichero de pruebas realizado con la versión 1.11.3 de Julia
println(VERSION)
#  y la 1.11.3 de Random
println(Random.VERSION)
#  y las versiones 0.14.25 de Flux, 1.0.2 de SymDoME y 0.20.0 de MLJ
import Pkg
Pkg.status("Flux")
Pkg.status("SymDoME")
Pkg.status("MLJ")

# Es posible que con otras versiones los resultados sean distintos, estando las funciones bien, sobre todo en la funciones que implican alguna componente aleatoria




# Cargamos el dataset
using DelimitedFiles: readdlm
dataset = readdlm("iris.data",',');
# Preparamos las entradas
inputs = convert(Array{Float32,2}, dataset[:,1:4]);
targets = dataset[:,5];


# ----------------------------------------------------------------------------------------------
# ------------------------------------- Ejercicio 4 --------------------------------------------
# ----------------------------------------------------------------------------------------------


(acc, errorRate, recall, specificity, precision, NPV, F1, confMatrix) = confusionMatrix(sin.(1:8).>=0, [falses(4); trues(4)]);
@assert(isapprox(acc, 0.375) && isapprox(errorRate, 1-0.375) && isapprox(recall, 0.5) && isapprox(specificity, 0.25) && isapprox(precision, 0.4) && isapprox(NPV, 1/3.) && isapprox(F1, 4/9.) && confMatrix==[1 3; 2 2])

(acc, errorRate, recall, specificity, precision, NPV, F1, confMatrix) = confusionMatrix(sin.(1:8), [falses(4); trues(4)]; threshold=0.9);
@assert(isapprox(acc, 0.5) && isapprox(errorRate, 0.5) && isapprox(recall, 0.25) && isapprox(specificity, 0.75) && isapprox(precision, 0.5) && isapprox(NPV, 0.5) && isapprox(F1, 1/3.) && confMatrix==[3 1; 3 1])

(acc, errorRate, recall, specificity, precision, NPV, F1, confMatrix) = confusionMatrix(Bool[1 0 0; 1 0 0; 1 0 0; 0 1 0; 0 1 0; 0 1 0; 0 0 1; 0 0 1; 0 0 1], Bool[1 0 0; 0 1 0; 0 0 1; 1 0 0; 0 1 0; 0 0 1; 1 0 0; 0 1 0; 0 0 1]; weighted=true)
@assert(isapprox(acc, 1/3.) && isapprox(errorRate, 2/3.) && isapprox(recall, 1/3.) && isapprox(specificity, 2/3.) && isapprox(precision, 1/3.) && isapprox(NPV, 2/3.) && isapprox(F1, 1/3.) && confMatrix==[1 1 1; 1 1 1; 1 1 1])

(acc, errorRate, recall, specificity, precision, NPV, F1, confMatrix) = confusionMatrix(Float64[1 0 0; 1 0 0; 1 0 0; 0 1 0; 0 1 0; 0 1 0; 0 0 1; 0 0 1; 0 0 1] .+ 1, Bool[1 0 0; 0 1 0; 0 0 1; 1 0 0; 0 1 0; 0 0 1; 1 0 0; 0 1 0; 0 0 1]; weighted=true)
@assert(isapprox(acc, 1/3.) && isapprox(errorRate, 2/3.) && isapprox(recall, 1/3.) && isapprox(specificity, 2/3.) && isapprox(precision, 1/3.) && isapprox(NPV, 2/3.) && isapprox(F1, 1/3.) && confMatrix==[1 1 1; 1 1 1; 1 1 1])

(acc, errorRate, recall, specificity, precision, NPV, F1, confMatrix) = confusionMatrix(repeat(unique(targets), 50), targets)
@assert(isapprox(acc, 1/3.) && isapprox(errorRate, 2/3.) && isapprox(recall, 1/3.) && isapprox(specificity, 2/3.) && isapprox(precision, 1/3.) && isapprox(NPV, 2/3.) && isapprox(F1, 1/3.) && confMatrix==[17 17 16; 17 16 17; 16 17 17])




outputs2Classes = trainClassDoME((inputs[1:100,:], targets[1:100].=="Iris-setosa"), inputs[[1],:], 20);
@assert(isapprox(outputs2Classes[1], 1.0751594373353253));

outputs3Classes = trainClassDoME((inputs[1:149,:], oneHotEncoding(targets[1:149])), inputs[[150],:], 20);
@assert(all(isapprox.(outputs3Classes, [-0.993565  -0.428653  0.113664]; rtol=1e-3)));

outputs3Classes = trainClassDoME((inputs[1:149,:], targets[1:149]), inputs[[150],:], 20);
@assert(outputs3Classes[1]=="Iris-virginica");







# ----------------------------------------------------------------------------------------------
# ------------------------------------- Ejercicio 5 --------------------------------------------
# ----------------------------------------------------------------------------------------------

using Random
using Random:seed!

# Establecemos la semilla para que los resultados sean siempre los mismos
using Random: seed!
# Comprobamos que la generación de números aleatorios es la esperada:
seed!(1); @assert(isapprox(rand(), 0.07336635446929285))
#  Si fallase aquí, seguramente dara error al comprobar los resultados de la ejecución de la siguiente función porque depende de la generación de números aleatorios





# Prueba con solamente una ejecucion de la RNA para cada fold, sin conjunto de validación
seed!(1); ((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    ANNCrossValidation([3], (inputs, targets), repeat(1:10, 15);
        numExecutions=1, maxEpochs=100, validationRatio=0, maxEpochsVal=5);
@assert(isapprox(testAccuracy_mean,    0.8733333333333334) && isapprox(testAccuracy_std,    0.14555131461166948))
@assert(isapprox(testErrorRate_mean,   0.12666666666666668) && isapprox(testErrorRate_std,   0.14555131461166948))
@assert(isapprox(testRecall_mean,      0.8733333333333334) && isapprox(testRecall_std,      0.14555131461166948))
@assert(isapprox(testSpecificity_mean, 0.9366666666666665) && isapprox(testSpecificity_std, 0.07277565730583475))
@assert(isapprox(testPrecision_mean,   0.9277777777777777) && isapprox(testPrecision_std,   0.06953697539080962))
@assert(isapprox(testNPV_mean,         0.9545454545454545) && isapprox(testNPV_std,         0.04719813390194002))
@assert(isapprox(testF1_mean,          0.8397306397306397) && isapprox(testF1_std,          0.198289533779536))
@assert(all(isapprox(testConfusionMatrix, [50.0 0.0 0.0; 0.0 37.0 13.0; 0.0 6.0 44.0])))



# Prueba similar a la anterior, pero con un vector de salidas deseadas con elementos que no son todos de tipo String
seed!(1); ((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    ANNCrossValidation([3], (inputs, map(x -> x=="Iris-setosa" ? 1 : x, targets)), repeat(1:10, 15);
        numExecutions=1, maxEpochs=100, validationRatio=0, maxEpochsVal=5);
# Los resultados deberían ser idénticos a los anteriores
@assert(isapprox(testAccuracy_mean,    0.8733333333333334) && isapprox(testAccuracy_std,    0.14555131461166948))
@assert(isapprox(testErrorRate_mean,   0.12666666666666668) && isapprox(testErrorRate_std,   0.14555131461166948))
@assert(isapprox(testRecall_mean,      0.8733333333333334) && isapprox(testRecall_std,      0.14555131461166948))
@assert(isapprox(testSpecificity_mean, 0.9366666666666665) && isapprox(testSpecificity_std, 0.07277565730583475))
@assert(isapprox(testPrecision_mean,   0.9277777777777777) && isapprox(testPrecision_std,   0.06953697539080962))
@assert(isapprox(testNPV_mean,         0.9545454545454545) && isapprox(testNPV_std,         0.04719813390194002))
@assert(isapprox(testF1_mean,          0.8397306397306397) && isapprox(testF1_std,          0.198289533779536))
@assert(all(isapprox(testConfusionMatrix, [50.0 0.0 0.0; 0.0 37.0 13.0; 0.0 6.0 44.0])))


# Para realizar las pruebas con conjunto de validación, se define de nuevo la función holdOut
#  Esta definición es incorrecta, pero se hace para que los resultados sean repetibles
holdOut(N::Int, P::Real) = (1:N)[1:Int(round(N*(1-P)))], (1:N)[Int(round(N*(1-P)))+1:end]


# Prueba con solamente una ejecucion de la RNA para cada fold, con conjunto de validación
seed!(1); ((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    ANNCrossValidation([3], (inputs, targets), repeat(1:10, 15);
        numExecutions=1, maxEpochs=100, validationRatio=0.2, maxEpochsVal=5);
@assert(isapprox(testAccuracy_mean,    0.31333333333333335) && isapprox(testAccuracy_std,    0.07062332703142535 ))
@assert(isapprox(testErrorRate_mean,   0.6866666666666668 ) && isapprox(testErrorRate_std,   0.07062332703142533 ))
@assert(isapprox(testRecall_mean,      0.31333333333333335) && isapprox(testRecall_std,      0.07062332703142533 ))
@assert(isapprox(testSpecificity_mean, 0.6566666666666667 ) && isapprox(testSpecificity_std, 0.03531166351571266 ))
@assert(isapprox(testPrecision_mean,   0.7047619047619047 ) && isapprox(testPrecision_std,   0.1563221222926793  ))
@assert(isapprox(testNPV_mean,         0.709126984126984  ) && isapprox(testNPV_std,         0.14906709044077748 ))
@assert(isapprox(testF1_mean,          0.1671998624011008 ) && isapprox(testF1_std,          0.050384177885437725))
@assert(all(isapprox(testConfusionMatrix, [12.0 18.0 20.0; 15.0 15.0 20.0; 15.0 15.0 20.0])))




# Prueba con varias ejecuciones en cada fold, con conjunto de validación
seed!(1); ((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    ANNCrossValidation([3], (inputs, targets), repeat(1:10, 15);
        numExecutions=10, maxEpochs=100, validationRatio=0.2, maxEpochsVal=5);
@assert(isapprox(testAccuracy_mean,    0.3546666666666667 ) && isapprox(testAccuracy_std,    0.04573676695889042))
@assert(isapprox(testErrorRate_mean,   0.6453333333333334) && isapprox(testErrorRate_std,   0.04573676695889043))
@assert(isapprox(testRecall_mean,      0.3546666666666667 ) && isapprox(testRecall_std,      0.04573676695889042))
@assert(isapprox(testSpecificity_mean, 0.6773333333333335 ) && isapprox(testSpecificity_std, 0.022868383479445226))
@assert(isapprox(testPrecision_mean,   0.7299271931771931   ) && isapprox(testPrecision_std,   0.039111651830628154))
@assert(isapprox(testNPV_mean,         0.7628573926073925  ) && isapprox(testNPV_std,         0.031091721114443215))
@assert(isapprox(testF1_mean,          0.21172955934101445 ) && isapprox(testF1_std,          0.04502371938130511))
@assert(all(isapprox(testConfusionMatrix, [19.6 14.9 15.5; 15.9 18.1 16.0; 14.8 19.7 15.5])))



 





# ----------------------------------------------------------------------------------------------
# ------------------------------------- Ejercicio 6 --------------------------------------------
# ----------------------------------------------------------------------------------------------




((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    modelCrossValidation(:DoME, Dict("maximumNodes" => 20), (inputs, targets), repeat(1:10, 15));
@assert(isapprox(testAccuracy_mean,    0.9533333333333335 ) && isapprox(testAccuracy_std,    0.032203059435976525))
@assert(isapprox(testErrorRate_mean,   0.046666666666666655) && isapprox(testErrorRate_std,   0.032203059435976525))
@assert(isapprox(testRecall_mean,      0.9533333333333335 ) && isapprox(testRecall_std,      0.032203059435976525))
@assert(isapprox(testSpecificity_mean, 0.9766666666666668 ) && isapprox(testSpecificity_std, 0.016101529717988314))
@assert(isapprox(testPrecision_mean,   0.9611111111111112   ) && isapprox(testPrecision_std,   0.026835882863313787))
@assert(isapprox(testNPV_mean,         0.9787878787878785  ) && isapprox(testNPV_std,         0.014637754289080304))
@assert(isapprox(testF1_mean,          0.9528619528619527 ) && isapprox(testF1_std,          0.032528342864622826))
@assert(all(isapprox(testConfusionMatrix, [49 1 0; 0 48 2; 0 4 46])))


((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    modelCrossValidation(:SVC,
        Dict(
            "C" => 1,
            "kernel" => "rbf",
            "gamma"  => 3),
        (inputs, targets), repeat(1:10, 15));
@assert(isapprox(testAccuracy_mean,    0.96               ) && isapprox(testAccuracy_std,    0.03442651863295481))
@assert(isapprox(testErrorRate_mean,   0.04               ) && isapprox(testErrorRate_std,   0.0344265186329548))
@assert(isapprox(testRecall_mean,      0.96               ) && isapprox(testRecall_std,      0.03442651863295481))
@assert(isapprox(testSpecificity_mean, 0.98               ) && isapprox(testSpecificity_std, 0.01721325931647746))
@assert(isapprox(testPrecision_mean,   0.9666666666666666 ) && isapprox(testPrecision_std,   0.028688765527462363))
@assert(isapprox(testNPV_mean,         0.9818181818181817 ) && isapprox(testNPV_std,         0.01564841756043409))
@assert(isapprox(testF1_mean,          0.9595959595959596 ) && isapprox(testF1_std,          0.03477426124540898))
@assert(all(isapprox(testConfusionMatrix, [49 0 1; 0 47 3; 0 2 48])))


((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    modelCrossValidation(:DecisionTreeClassifier, Dict("max_depth" => 4), (inputs, targets), repeat(1:10, 15));
@assert(isapprox(testAccuracy_mean,    0.9466666666666669) && isapprox(testAccuracy_std,    0.052587375849774354))
@assert(isapprox(testErrorRate_mean,   0.05333333333333332) && isapprox(testErrorRate_std,   0.052587375849774354))
@assert(isapprox(testRecall_mean,      0.9466666666666667) && isapprox(testRecall_std,      0.05258737584977439))
@assert(isapprox(testSpecificity_mean, 0.9733333333333334) && isapprox(testSpecificity_std, 0.02629368792488719))
@assert(isapprox(testPrecision_mean,   0.9587301587301589) && isapprox(testPrecision_std,   0.03866418181258228))
@assert(isapprox(testNPV_mean,         0.9767676767676768) && isapprox(testNPV_std,         0.02223242292150734))
@assert(isapprox(testF1_mean,          0.9452861952861952) && isapprox(testF1_std,          0.054551689380537616))
@assert(all(isapprox(testConfusionMatrix, [50 0 0; 0 47 3; 0 5 45])))
    

((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    modelCrossValidation(:KNeighborsClassifier, Dict("n_neighbors" => 3), (inputs, targets), repeat(1:10, 15));
@assert(isapprox(testAccuracy_mean,    0.9666666666666668) && isapprox(testAccuracy_std,    0.03513641844631532))
@assert(isapprox(testErrorRate_mean,   0.0333333333333333) && isapprox(testErrorRate_std,   0.03513641844631532))
@assert(isapprox(testRecall_mean,      0.9666666666666668) && isapprox(testRecall_std,      0.03513641844631532))
@assert(isapprox(testSpecificity_mean, 0.9833333333333334) && isapprox(testSpecificity_std, 0.017568209223157716))
@assert(isapprox(testPrecision_mean,   0.9722222222222223) && isapprox(testPrecision_std,   0.029280348705262787))
@assert(isapprox(testNPV_mean,         0.9848484848484848) && isapprox(testNPV_std,         0.01597109929377977))
@assert(isapprox(testF1_mean,          0.9663299663299663) && isapprox(testF1_std,          0.035491331763954956))
@assert(all(isapprox(testConfusionMatrix, [50 0 0; 0 47 3; 0 2 48])))


seed!(1); ((testAccuracy_mean, testAccuracy_std), (testErrorRate_mean, testErrorRate_std), (testRecall_mean, testRecall_std), (testSpecificity_mean, testSpecificity_std), (testPrecision_mean, testPrecision_std), (testNPV_mean, testNPV_std), (testF1_mean, testF1_std), testConfusionMatrix) =
    modelCrossValidation(:ANN,
        Dict(
            "topology"        => [4, 3],
            "learningRate"    => 0.01,
            "validationRatio" => 0.2,
            "numExecutions"   => 50,
            "maxEpochs"       => 100,
            "maxEpochsVal"     => 20),
        (inputs, targets), repeat(1:10, 15));
@assert(isapprox(testAccuracy_mean,    0.348            ) && isapprox(testAccuracy_std,    0.012204026860218656))
@assert(isapprox(testErrorRate_mean,   0.652            ) && isapprox(testErrorRate_std,   0.012204026860218648))
@assert(isapprox(testRecall_mean,      0.348            ) && isapprox(testRecall_std,      0.012204026860218656))
@assert(isapprox(testSpecificity_mean, 0.674            ) && isapprox(testSpecificity_std, 0.006102013430109324))
@assert(isapprox(testPrecision_mean,   0.7696506456506453) && isapprox(testPrecision_std,   0.003526843563719326))
@assert(isapprox(testNPV_mean,         0.777215007215007) && isapprox(testNPV_std,         0.0044380494173253725))
@assert(isapprox(testF1_mean,          0.18758329332632737) && isapprox(testF1_std,          0.01437405343817687))
@assert(all(isapprox(testConfusionMatrix, [18.2 14.94 16.86; 15.92 17.1 16.98; 15.82 17.28 16.9])))


