# Guía: Cómo Ejecutar Código C# en un Ordenador Nuevo

El objetivo de esta nota es detallar, paso a paso, cómo configurar un entorno desde cero en un ordenador con Windows para poder compilar y ejecutar código C#. A diferencia de lenguajes como Python, C# es un lenguaje compilado que forma parte del ecosistema .NET, por lo que requiere una instalación previa de herramientas específicas.

## Paso 1: Instalar el SDK de .NET

El primer y más importante paso es instalar el **SDK (Software Development Kit) de .NET**. Esto nos da el compilador y todo lo necesario para crear y ejecutar código.

### Método 1: Usando Scoop (Recomendado)
Si usas el gestor de paquetes **Scoop**, la instalación es mucho más limpia, sencilla y no suele requerir permisos de administrador.

```powershell
scoop install dotnet-sdk
```
> Si no tienes o no sabes qué es Scoop, consulta esta guía: [Cómo Instalar y Usar Scoop](001_scoop_package_manager.md).

### Método 2: Manual (Tradicional)
1.  **Ir a la web oficial:** Accede a la página de descargas de .NET: [https://dotnet.microsoft.com/download](https://dotnet.microsoft.com/download).
2.  **Descargar el SDK:** Busca y descarga la versión más reciente que sea **LTS (Long-Term Support)**.
3.  **Instalar:** El proceso es un asistente estándar de Windows. Simplemente sigue los pasos hasta que finalice.

## Paso 2: Verificar la Instalación

Para confirmar que .NET se ha instalado correctamente, abre una nueva terminal (PowerShell o Símbolo del sistema) y ejecuta el siguiente comando:

```powershell
dotnet --version
```

Si la instalación fue exitosa, verás en pantalla el número de la versión del SDK que acabas de instalar (por ejemplo, `8.0.100`).

## Paso 3: Crear y Ejecutar un Programa

La forma recomendada de trabajar en C# es a través de "proyectos". El SDK de .NET nos da comandos para gestionar esto fácilmente.

### A. Crear el Proyecto

1.  Crea una carpeta para tu nuevo proyecto y navega hacia ella en la terminal.
    ```powershell
    mkdir MiPrimeraApp
    cd MiPrimeraApp
    ```
2.  Dentro de la carpeta, ejecuta el siguiente comando para crear un nuevo proyecto de tipo "aplicación de consola":
    ```powershell
    dotnet new console
    ```
    Este comando generará dos archivos principales:
    *   `Program.cs`: Aquí es donde escribirás tu código C#.
    *   `MiPrimeraApp.csproj`: Es el archivo de configuración del proyecto.

### B. Revisar el Código

Si abres el archivo `Program.cs` con cualquier editor de texto, verás un "Hola Mundo" por defecto:

```csharp
// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");
```

### C. Compilar y Ejecutar

Ahora viene la magia. Desde la carpeta de tu proyecto (`MiPrimeraApp`), ejecuta:

```powershell
dotnet run
```

Este único comando hace dos cosas:
1.  **Compila** todo el código C# de tu proyecto en un programa ejecutable.
2.  **Ejecuta** ese programa recién compilado.

Verás la salida `"Hello, World!"` en tu terminal.

---

## Resumen del Flujo de Trabajo

1.  **Instalar SDK de .NET** (una sola vez por ordenador).
2.  Crear una nueva carpeta y ejecutar **`dotnet new console`** para iniciar un proyecto.
3.  Escribir tu lógica en el archivo `Program.cs`.
4.  Ejecutar **`dotnet run`** desde la carpeta del proyecto para compilar y ver el resultado.
