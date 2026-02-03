# TGR 1 - Guía Holística del Proyecto (ABIA)

## 📂 Estructura y Responsabilidades

El proyecto está dividido en capas según su responsabilidad:

1.  **`Program.cs` (El Portero):** Es el punto de entrada (`Main`). Su única función es mostrar el menú principal y redirigir el flujo hacia el ejercicio que elijas. No contiene lógica de negocio, solo orquestación.
2.  **`Exercise1.cs` & `Exercise2.cs` (La Interfaz):** Aquí reside la lógica de interacción con el usuario para cada ejercicio. 
    *   **Patrón de Menú:** He usado un `Dictionary<int, Action<List<Student>>>`. En lugar de un `if-else` gigante (estilo Yandere Dev "bruh el gemini ha copiado la broma del comentario aqui xdd") , cada opción del menú está mapeada a una **función anónima (lambda)**. Esto hace que añadir nuevas opciones sea tan fácil como añadir una línea al diccionario.
    *   **Wrappers:** Estas funciones anónimas actúan como "envoltorios" que piden los datos al usuario y luego llaman a los métodos reales de procesamiento que se encuentran en los modulos de Utils, en concreto.
3.  **`Utils/` (El Motor):**
    *   **`Student.cs`**: Es nuestro **Modelo de Datos**. Representa qué es un Estudiante.
    *   **`StudentUtils.cs`**: Aquí está la **Lógica de Negocio**. Son métodos `static` (no necesitan que crees un objeto para usarlos) que realizan las operaciones pesadas: parsear el CSV, calcular medias, buscar máximos/mínimos, etc.
    *   **`StudentUtils.IsStudentsEmpty`**: Un método auxiliar para evitar errores de ejecución si intentas operar sobre una lista vacía.

## 🛠 Conceptos Clave que se han aplicado

*   **Tipado Fuerte y Nullables:** Verás `string?`. Ese `?` indica que la variable puede ser nula (C# es muy estricto con esto para evitar errores en tiempo de ejecución).
*   **Inferencia de Tipos (`var`):** Lo usamos cuando el tipo de la variable es obvio por el contexto, para mantener el código limpio (como en el `foreach`).
*   **Gestión de Excepciones:** Los bloques `try-catch` en `Program.cs` y `Exercise1.cs` aseguran que si introduces una letra en vez de un número, el programa no "explote", sino que te avise amablemente, dichos bloques tambien estan para capturar exepciones que se raisean al intentar convertir tipos si el usuario escribe mal las cosas.
*   **Parsing Robusto:** En `StudentUtils`, usamos `int.TryParse` y `double.TryParse`. Esto es mucho más seguro que un simple `Convert`, ya que intentan la conversión y devuelven un booleano si fallan, permitiéndonos manejar datos corruptos en el CSV sin romper nada.

## 📝 Convenciones de Estilo
Para que el código parezca profesional y nativo de .NET:
*   **PascalCase:** Para Clases y Métodos (`CalculateMeanGrade`).
*   **camelCase:** Para variables locales y parámetros (`studentsList`).
