# Argumentos en argparse: Posicionales, Keyword y Flags

## Resumen Ejecutivo

| Tipo | Sintaxis | Obligatorio | Valor por defecto | Ejemplo |
|------|----------|-------------|------------------|---------|
| **Posicional** | `parser.add_argument('nombre')` | ✅ Sí | No tiene | `python script.py archivo.txt` |
| **Keyword (Opcional)** | `add_argument('-f', '--file')` | ❌ No | `None` | `python script.py --file=test.txt` |
| **Flag** | `add_argument('--verbose')` | ❌ No | `False` | `python script.py --verbose` |

---

## 1. Argumentos Posicionales (Obligatorios)

### Características:
- Se pasan en orden, sin prefijo `-`
- **Siempre obligatorios** a menos que se defina un valor por defecto
- No tienen nombre asociado

### Ejemplo:
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help="Archivo de entrada")
parser.add_argument('output_file', help="Archivo de salida")

args = parser.parse_args()
# args.input_file  → "entrada.txt"
# args.output_file → "salida.txt"
```

### Comportamiento:
```bash
$ python script.py entrada.txt salida.txt    # ✅ Correcto
$ python script.py                          # ❌ Error: argument missing
```

---

## 2. Keyword Arguments (Opcionales con Nombre)

### Características:
- Se pasan con prefijo `-` o `--`
- **No obligatorios** → valor por defecto es `None`
- Tienen nombre asociado que se accede como atributo

### Sintaxis:
```python
parser.add_argument(
    '-f', '--file',      # Corta y larga
    dest='filename',     # Nombre del atributo en args
    help="Archivo de configuración"
)
```

### Comportamiento:
```bash
$ python script.py --file=config.txt        # ✅ Con valor
$ python script.py                          # ✅ Sin valor → None
```

En Python:
```python
print(args.file)  # "config.txt" o None
if args.file:     # Funciona porque None es falsy
    print(f"Usando {args.file}")
```

---

## 3. Flags (Banderas Opcionales)

### Características:
- No toman valor, solo indican presencia/ausencia
- **No obligatorios** → valor por defecto es `False` o `None`
- Se acceden como booleanos

### Dos formas de crear flags:

#### Forma A: Con `action='store_true'`
```python
parser.add_argument('-v', '--verbose', action='store_true')
```

#### Forma B: Sin parámetros (más simple)
```python
parser.add_argument('-v', '--verbose')  # Implícitamente store_true
```

### Comportamiento:
```bash
$ python script.py --verbose               # args.verbose = True
$ python script.py                         # args.verbose = False
```

---

## 4. Comparación Práctica

### Código de ejemplo:
```python
import argparse

parser = argparse.ArgumentParser(description="Ejemplo completo")

# Posicional (obligatorio)
parser.add_argument('archivo', help="Archivo a procesar")

# Keyword opcional con valor
parser.add_argument('-o', '--output', default='salida.txt')

# Flag opcional
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
```

### Tabla de resultados:

| Comando | `archivo` | `output` | `debug` |
|---------|-----------|----------|--------|
| `python script.py data.txt` | "data.txt" | "salida.txt" | False |
| `python script.py data.txt -o out.dat --debug` | "data.txt" | "out.dat" | True |

---

## 5. El Truco de `required=True`

Puedes convertir un argumento opcional en obligatorio:

```python
# Opcional por defecto
parser.add_argument('-f', '--file')

# Obligatorio (como si fuera posicional)
parser.add_argument('-f', '--file', required=True)
```

### Comportamiento:
```bash
$ python script.py                          # ❌ Error: the following arguments are required: -f/--file
$ python script.py --file=test.txt          # ✅ Correcto
```

---

## 6. Flags Mutuamente Excluyentes

### Sintaxis:
```python
grupo = parser.add_mutually_exclusive_group(required=True)
grupo.add_argument('-d', action='store_true')
grupo.add_argument('-i', action='store_true')
grupo.add_argument('-w', action='store_true')
```

### Reglas:
1. ✅ **Máximo 1 flag** del grupo puede estar presente
2. ✅ `required=True` → Al menos 1 debe estar presente
3. ❌ Múltiples flags activas = Error
4. ❌ Ninguna activa (con required) = Error

### Ejemplo en el código:
```bash
# ✅ Correcto - solo una opción
$ python nafda.py -d jojos.bin
$ python nafda.py -i jojos.bin
$ python nafda.py -w jojos.bin

# ❌ Incorrecto - múltiples opciones
$ python nafda.py -d -i jojos.bin  # Error: argument -i not allowed with argument -d

# ❌ Incorrecto - ninguna opción (con required=True)
$ python nafda.py jojos.bin        # Error: one of the arguments is required
```

---

## 7. Diagrama de Flujo de Parsing

```mermaid
graph TD
    A[Usuario escribe comando] --> B{Argumentos presentes?}
    B -->|Posicional sin valor| C[Error]
    B -->|Opcional sin valor| D[Usar default: None/False]
    B -->|Flag con -v|--| E[Activar flag: True]
    B -->|Keyword con --file=x| F[Asignar valor a atributo]
    
    G{required=True?}
    G -->|Sí y faltan args| C
    G -->|No o todos presentes| H[Crear objeto args]
    H --> I[Devolver args namespace]
```

---

## 8. Valores por Defecto Personalizados

```python
# Default explícito
parser.add_argument('-c', '--count', default=10)

args = parser.parse_args([])  # args.count = 10

# Usando type() para transformar el valor
parser.add_argument('-n', '--number', type=int, default=0)
```

---

## 9. Resumen de `action` Parameters

| action | Comportamiento |
|--------|---------------|
| `'store_true'` | Flag → True si presente, False si no |
| `'store_false'` | Inverso: False si presente, True si no |
| `'store_const'` | Guarda valor constante (ej. `const=42`) |
| `'append'` | Añade múltiples veces a una lista |
| `'count'` | Cuenta apariciones del flag |

---

## 10. Verificación en el Código Original

### En `nafda.py`:
```python
# Línea 183-186: Grupo mutuamente excluyente
grupo = parser.add_mutually_exclusive_group(required=True)
grupo.add_argument('-d', action='store_true')
grupo.add_argument('-i', action='store_true')
grupo.add_argument('-w', action='store_true')

# Línea 189: Argumento posicional obligatorio
parser.add_argument('input_bin', help="...")
```

### Resultado en `args`:
```python
args = Namespace(
    input_bin='jojos.bin',      # Posicional
    d=False,                    # Flag (por defecto)
    i=False,                    # Flag (por defecto)
    w=False                     # Flag (por defecto)
)
```

---

## 11. Comprobación de Tipos en Python

```python
# Flags y keywords sin valor son falsy pero distintos
print(bool(None))      # False
print(bool(False))     # False
print(None == False)   # False (¡son diferentes!)

# Por eso usar 'if args.flag:' es seguro:
if args.debug:         # Funciona para ambos casos
    print("Debug mode")
```

---

## 12. Best Practices

### ✅ Buena práctica:
```python
parser.add_argument('-o', '--output', default='salida.txt')
# Permite detectar si el usuario lo especificó explícitamente
if args.output != 'salida.txt':
    print("Usuario proporcionó output personalizado")
```

### ❌ Mala práctica:
```python
parser.add_argument('-o', '--output')  # Sin default
# args.output será None, no hay forma de distinguir
# entre "no pasado" y "pasado como None"
```

---

## Referencia Rápida

| Concepto | Síntaxis | Default | Tipo en `args` |
|----------|----------|---------|---------------|
| Posicional | `'nombre'` | N/A | String/Any |
| Keyword | `'-f', '--file'` | `None` | Any (incl. None) |
| Flag | `'-v'` con `store_true` | `False` | Booleano |

---

*Nota: Esta documentación es local y específica del proyecto ALF p2.*
