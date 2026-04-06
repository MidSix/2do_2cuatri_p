# Instrucciones SIMD y Registros Anchos

## 1. ¿Qué significa **SIMD**?

- **S**ingle Instruction, **M**ultiple Data.
- Una *única* instrucción de la CPU opera sobre varios valores al mismo tiempo (p.ej., sumar cuatro enteros o cuatro flotantes).
- Se usa para aprovechar el paralelismo a nivel de datos dentro de un solo ciclo de reloj.

## 2. Registros anchos

| Arquitectura | Unidad de palabra | Registro SIMD típico | Tamaño |
|--------------|-------------------|----------------------|--------|
| x86 (Intel/AMD) | 32 bits | XMM, YMM, ZMM | 128 / 256 / 512 bits |
| ARM v7–v8 | 32 bits | NEON `q0`‑`q15` | 128 bits |
| PowerPC (Altivec/VSX) | 32 bits | VSR‑0…VSR‑31 | 128 / 256 bits |

### ¿Por qué 128 bits como mínimo?
- **Paralelismo útil**: con una palabra de 32 bits, un registro de 128 bits permite al menos 4 lanes paralelos.
- **Compatibilidad con bus y caché**: la mayoría de sistemas de 32‑bit usan buses de 64 bits y líneas de caché de 64 bytes; 128 bits se ajusta bien a dos palabras de 64 bits o cuatro de 32 bits sin desalineación.
- **Simplicidad de implementación**: agrupar unidades scalaras ya existentes (por ejemplo, 4 ALUs de 32 bits) evita complejidades extra y mantiene el pipeline lineal.
- **Balance rendimiento‑costo**: más allá de 128 bits el hardware se vuelve significativamente más caro en consumo eléctrico y área física sin un retorno proporcional de rendimiento para la mayoría de aplicaciones.

## 3. Ejemplo práctico (x86 SSE)
```asm
; XMM registers hold 4 single‑precision floats each
; xmm0 = {a3, a2, a1, a0}
; xmm1 = {b3, b2, b1, b0}
addps   xmm0, xmm1      ; SIMD: suma los 4 pares simultáneamente
```
Correspondiente código C con intrinsics:
```c
#include <immintrin.h>
__m128 a = _mm_set_ps(4.0f, 3.0f, 2.0f, 1.0f);   // {a3,a2,a1,a0}
__m128 b = _mm_set_ps(8.0f, 7.0f, 6.0f, 5.0f);   // {b3,b2,b1,b0}
__m128 c = _mm_add_ps(a, b);                      // SIMD suma cuatro floats a la vez
```
Resultado:
```
c = {12.0f, 10.0f, 8.0f, 6.0f}
```
### Relación con el acrónimo
- **Single Instruction**: `addps` o `_mm_add_ps` es la única instrucción que se ejecuta.
- **Multiple Data**: los cuatro pares de números (`a3+b3`, `a2+b2`, …) se procesan en paralelo dentro del mismo registro SIMD.

## 4. Resumen
- **SIMD** promueve el paralelismo a nivel de datos, aumentando la eficiencia sin aumentar la complejidad del algoritmo.
- Los **registros anchos** (≥ 128 bits) son esenciales para que una sola instrucción pueda operar sobre múltiples lanes; su tamaño está elegido por un balance entre rendimiento y costo de hardware.
- El ejemplo con SSE muestra cómo una única línea de ensamblador o C intrínseca puede procesar cuatro valores simultáneamente, ilustrando el poder del enfoque SIMD.

---
**Autor:** [Tu Nombre]
**Curso:** Computación Concurrente, Paralela y Distribuida – Práctica 4
**Fecha:** 2026-03-22