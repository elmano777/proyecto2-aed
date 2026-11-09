# DFS Timestamps (tin / tout)

Proyecto Final 2 – CS2023 Algoritmos y Estructuras de Datos (2026-2) · UTEC

**Integrantes:**
- Aguirre Milla, Fernando
- Díaz Jara, Rolando David
- Velásquez Díaz, Eliseo David

## Descripción

Video educativo, al estilo de Manim, que explica los **tiempos de descubrimiento (`tin`)
y finalización (`tout`)** de un DFS y cómo permiten decidir en **O(1)** si un nodo es
ancestro de otro (o si pertenece a su subárbol) después de un único DFS en **O(n)**.

La animación **no está hecha a mano**: la implementación en C++ (`cpp/dfs_timestamps.cpp`)
ejecuta el DFS y escribe una *traza* de eventos en JSON (`enter u`, `exit u`, consultas).
La escena de Manim (`animation/escena.py`) lee esa traza, calcula cómo dibujar el árbol y
anima cada evento. Si se cambia el árbol de entrada, cambia la animación.

## La implementación

Un reloj global aumenta en 1 al **entrar** a un nodo (`tin`) y en 1 al **salir** (`tout`).
El subárbol de `u` ocupa el intervalo `[tin[u], tout[u]]`, y los intervalos de dos nodos están
anidados o son disjuntos. Por eso:

```
u es ancestro de v  <=>  tin[u] <= tin[v]  y  tout[v] <= tout[u]
```

El DFS es **iterativo** (pila explícita), así una cadena de 200000 nodos no agota la pila de
llamadas, que es el peor caso de un DFS recursivo. Los `tin`/`tout` salen idénticos a los de
la versión recursiva.

## Contenido del video (≈ 1.5 min, 1080p)

1. Título e integrantes
2. Introducción conceptual (qué son `tin`/`tout` y para qué sirven)
3. Demostración animada sobre un árbol de 7 nodos + consultas `es_ancestro`
4. Intervalos `[tin, tout]` anidados
5. Casos borde: un solo nodo y cadena (peor caso de profundidad)
6. Análisis de complejidad y créditos

## Estructura del repositorio

```
cpp/dfs_timestamps.cpp   DFS iterativo con tin/tout + generador de traza JSON
data/                    árboles de entrada (caso principal y casos borde)
animation/escena.py      escena de Manim que consume las trazas
scripts/run_all.py       compila, genera trazas y renderiza el video
scripts/test_dfs.py      pruebas del algoritmo (ver "Pruebas")
```

## Requisitos

- `g++` con soporte C++17
- Python 3.10+
- [Manim Community](https://docs.manim.community/en/stable/installation.html)
  (`pip install -r animation/requirements.txt`) y FFmpeg
- La escena usa solo `Text`, no requiere LaTeX
- En Linux, Manim necesita además Pango y Cairo:
  `sudo apt install libpango1.0-dev libcairo2-dev pkg-config python3-dev`

## Cómo ejecutar

```bash
git clone https://github.com/elmano777/proyecto2-aed.git
cd proyecto2-aed
pip install -r animation/requirements.txt
python scripts/run_all.py        # 1080p. Usa "python scripts/run_all.py l" para una prueba rápida
```

El video queda en `media/videos/escena/1080p60/DFSTimestamps.mp4`.

Para probar solo el C++ con otro árbol:

```bash
g++ -O2 -std=c++17 cpp/dfs_timestamps.cpp -o dfs_timestamps
./dfs_timestamps < data/arbol_ejemplo.txt           # SI / NO por consulta
./dfs_timestamps --trace < data/arbol_ejemplo.txt   # traza JSON para la animación
```

Formato de entrada: `n q`, luego `n-1` aristas (`u v`, nodos 1..n, raíz 1),
luego `q` consultas `u v` ("¿u es ancestro de v?").

## Pruebas

```bash
python scripts/test_dfs.py
```

Compila el C++ y comprueba: (1) los tres casos de `data/` con resultados esperados;
(2) 2000 árboles aleatorios, comparando `es_ancestro` contra una referencia independiente
(subir por los padres) y verificando que los tiempos sean exactamente 1..2n con `tin < tout`;
(3) una cadena de 200000 nodos.

## Complejidad

| Operación | Tiempo | Memoria |
|-|-|-|
| Construcción de `tin`/`tout` (un DFS) | O(n) | O(n) |
| `es_ancestro(u, v)` | O(1) | — |
| Tamaño del subárbol de `v`: `(tout[v] - tin[v] + 1) / 2` | O(1) | — |

## Video

Enlace: https://drive.google.com/file/d/1_-3wdxJ5AtUchLIoYprZp5We4xN_JAeD/view?usp=sharing

## Referencias

- Manim Community Documentation: https://docs.manim.community/
- Material del curso CS2023 (UTEC): concepto de tiempos de entrada y salida en un DFS
- Canal 3Blue1Brown (inspiración de estilo): https://www.3blue1brown.com/