import timeit

# Simulamos las coordenadas de 10 reinas (una lista de tuplas)
coords_originales = [(i, (i * 2) % 10) for i in range(10)]

# 1. Test de Creación/Conversión
def test_crear_lista():
    return list(coords_originales)

def test_crear_tupla():
    return tuple(coords_originales)
    
def test_crear_string():
    return str(coords_originales)

 # 2. Test de Comparación (Lo que hace el algoritmo miles de veces)
lista_a = list(coords_originales)
lista_b = list(coords_originales)
tupla_a = tuple(coords_originales)
tupla_b = tuple(coords_originales)
str_a = str(coords_originales)
str_b = str(coords_originales)

def comparar_listas():
    return lista_a == lista_b

def comparar_tuplas():
    return tupla_a == tupla_b

def comparar_strings():
    return str_a == str_b

 # Ejecución de las pruebas (1 millón de veces cada una)
N = 1_000_000

print(f"--- RESULTADOS (1 millón de ejecuciones) ---")
print(f"Crear Lista:   {timeit.timeit(test_crear_lista, number=N):.4f} segundos")
print(f"Crear Tupla:   {timeit.timeit(test_crear_tupla, number=N):.4f} segundos")
print(f"Crear String:  {timeit.timeit(test_crear_string, number=N):.4f} segundos (¡MUY LENTO!)")

print(f"\n--- TEST DE COMPARACIÓN (==) ---")
print(f"Comparar Listas:  {timeit.timeit(comparar_listas, number=N):.4f} segundos")
print(f"Comparar Tuplas:  {timeit.timeit(comparar_tuplas, number=N):.4f} segundos")