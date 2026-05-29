# TDA-TP3 - Problemas NP-Completos

Hitting Set es un problema que consiste en elegir un subconjunto `C` de un 
conjunto `A` tal que `C` interseque a todos los subconjuntos `B_i`. En la 
version de optimizacion, se busca que `C` tenga tamaño minimo.

En este TP, `A` son los jugadores, cada `B_i` es un pedido de la prensa y `C`
es el conjunto de jugadores elegidos para cubrir todos los pedidos. La parte
teorica usa la version de decision con un valor `k`; la parte practica busca
el optimo con backtracking.

**Informe: `agregar link`**

## Dependencias

Para correr el algoritmo de backtracking:

```bash
python3 tp3.py archivos-test-catedra/5.txt
```

Para correr programacion lineal, aproximacion por variables reales o graficos,
es necesario:

```bash
pip install pulp matplotlib
```

## Ejecutar el programa principal

```bash
python3 tp3.py ruta/a/listado.txt
```

Por ejemplo:

```bash
python3 tp3.py archivos-test-catedra/5.txt
python3 tp3.py archivos-test-catedra/200.txt
```

La salida muestra la cantidad minima encontrada y los jugadores elegidos.

## Generar instancias propias

Para generar los archivos de benchmark propios:

```bash
python3 generador_datos.py
```

Esto crea instancias en:

```text
archivos-test-propios/
```

Los benchmarks estan separados en tres experimentos:

```text
varia_n         -> cambia n y deja m fijo
varia_m         -> cambia m y deja n fijo
crecen_juntos   -> cambian n y m juntos, con m = 2n
```

Y en tres tipos de instancia:

```text
facil       -> hay jugadores que cubren muchos pedidos
aleatorio   -> pedidos generados al azar
dificil     -> pedidos chicos y con menos solapamiento
```

## Correr mediciones

Para correr los benchmarks y guardar los tiempos:

```bash
python3 mediciones.py
```

Esto genera:

```text
resultados-propios/resultados_mediciones.csv
```

El CSV incluye:

```text
experimento, tipo, algoritmo, n, m, solucion_tam, optimo, ratio, tiempo_promedio, valida
```

## Generar graficos

Despues de correr las mediciones:

```bash
python3 resultados-propios/graficar_benchmark.py
```

Esto genera estos graficos:

```text
resultados-propios/bt_varia_n_m_fijo.png
resultados-propios/bt_varia_m_n_fijo.png
resultados-propios/bt_crecen_juntos.png
resultados-propios/comparacion_tiempos_algoritmos.png
resultados-propios/comparacion_calidad_algoritmos.png
```