# Explicación Técnica: Método `SaveStudentsToCsv`

Este documento detalla el funcionamiento del método de persistencia para defenderlo ante el profesor.

## 1. Firma del método
```csharp
public static void SaveStudentsToCsv(string filePath, List<Student> students)
```
*   **`public static`**: Método utilitario. No requiere instanciar `StudentUtils`.
*   **`string filePath`**: La ruta destino (relativa o absoluta).
*   **`List<Student> students`**: Los datos en memoria a persistir.

## 2. Bloque `try-catch` (Control de Errores)
```csharp
try { ... } catch (Exception ex) { ... }
```
*   **Defensa**: Las operaciones I/O son **peligrosas** (disco lleno, permisos, ruta inválida). El bloque `try-catch` evita que el programa se cierre abruptamente (*crash*) y permite mostrar un error controlado.

## 3. Normalización de la Ruta (Robustez)
```csharp
if (filePath.TrimEnd().EndsWith(Path.DirectorySeparatorChar) || 
    filePath.TrimEnd().EndsWith(Path.AltDirectorySeparatorChar) ||
    Directory.Exists(filePath))
{
    string defaultName = "StudentList.csv";
    filePath = Path.Combine(filePath, defaultName);
}
```
*   **El Problema**: Si el usuario pasa una carpeta (`C:\Data\`), intentar escribir en ella lanza "Access Denied".
*   **La Solución**: Detectamos si es un directorio y usamos `Path.Combine` para añadir un nombre de archivo por defecto (`StudentList.csv`), convirtiendo la ruta de carpeta en una ruta de archivo válida.

## 4. Creación de Directorios (Robustez)
```csharp
string? parentDir = Path.GetDirectoryName(filePath);
if (!string.IsNullOrEmpty(parentDir) && !Directory.Exists(parentDir))
{
    Directory.CreateDirectory(parentDir);
}
```
*   **El Problema**: `StreamWriter` falla si la carpeta contenedora no existe.
*   **La Solución**: `Directory.CreateDirectory` crea **toda la jerarquía** necesaria recursivamente antes de escribir.

## 5. Escritura Segura: El patrón `using`
```csharp
using (StreamWriter writer = new StreamWriter(filePath))
{
    // ... escritura
}
```
*   **Concepto Clave**: Gestión de recursos no administrados (`IDisposable`).
*   **Defensa**: `using` garantiza que el archivo se **cierre (Dispose)** y libere la memoria tanto si la escritura es exitosa como si ocurre un error, evitando bloqueos de archivo.

## 6. Serialización y Cultura
```csharp
foreach (var s in students)
{
    string line = $"{s.Name}, {s.Age}, {s.Grade.ToString(CultureInfo.InvariantCulture)}";
    writer.WriteLine(line);
}
```
*   **`CultureInfo.InvariantCulture`**: Fuerza el uso del **punto decimal** (`7.5`) en lugar de la coma (`7,5`), independientemente de la configuración regional del PC (España vs USA).
*   **Por qué**: En un CSV (*Comma Separated Values*), usar una coma decimal rompería la estructura de columnas.

```