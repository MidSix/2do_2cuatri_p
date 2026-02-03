# 008_division_Casting

**Etiquetas:** #csharp #tipos #casting #python_vs_csharp

## 1. Promoción Implícita (La regla del "Más Preciso")
Sí, tu intuición es correcta. C# permite operaciones entre tipos numéricos distintos sin que hagas nada manual, siempre que no haya riesgo de perder datos. La regla es que el compilador **promueve automáticamente al tipo más preciso (menos restrictivo)**.

- `int` + `float` → `float`
- `int` + `double` → `double`
- `float` + `double` → `double`

```csharp
int entero = 5;
float decimal = 2.5f;

// C# convierte 'entero' a 5.0f internamente y luego suma.
float resultado = entero + decimal; // 7.5
```

## 2. El problema de la División de Enteros
El error que experimentaste ocurre porque **el tipo de retorno de una operación depende exclusivamente de los operandos**, no de la variable donde guardes el resultado.
```csharp
	//Codigo original
    internal static float mean_of_three(int[] array)
    {
        int array_len = array.Length;
        int total_sum = 0;
        for (int i = 0; i < array_len; i++)
        {
            total_sum+=array[i];
        }
        float mean_of_three = total_sum / array_len;
        return mean_of_three;
    }
```

- En tu código original: `total_sum / array_len`
- Ambos eran `int`.
- Por tanto, C# realiza el equivalente en python a una **división entera** (descarta el resto/decimales inmediatamente).
- Resultado: `7 / 2` es `3` (entero).
- Solo *después* de terminar la división, ese `3` se guardaba en tu variable `float`, convirtiéndose en `3.0`.

## 3. Casting Explícito (Conversión Forzada)
El **Casting** es poner `(tipo)` delante de un valor. Es una orden directa al compilador: *"Trata esta variable como si fuera de este otro tipo solo para esta operación"*.

Al hacer `(float)total_sum`:
1.  Transformas temporalmente el entero en un flotante.
2.  La operación se convierte en `float / int`.
3.  Aplicando la regla del punto 1, C# promueve el segundo `int` a `float`.
4.  Resultado: `float / float` = División con decimales correcta.

> **Diferencia con Python:**
> *   **Python:** El operador `/` siempre devuelve float (`5 / 2 == 2.5`). Para división entera usas `//`.
> *   **C#:** El operador `/` es polimórfico. Se comporta distinto según si divides enteros o flotantes.
