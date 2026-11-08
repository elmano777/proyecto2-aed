# DFS Timestamps (tin / tout)

Proyecto Final 2 – CS2023 Algoritmos y Estructuras de Datos (2026-2) · UTEC

**Integrantes:** Fernando Aguirre Milla  · Rolando David Diaz Jara · Eliseo David Velasquez Diaz 

Descripción

Video educativo, al estilo de Manim, que explica los **tiempos de descubrimiento (`tin`)
y finalización (`tout`)** de un DFS y cómo permiten decidir en **O(1)** si un nodo es
ancestro de otro (o si pertenece a su subárbol) tras un único DFS en **O(n)**.

La animación **no está hecha a mano**: la implementación en C++
(`cpp/dfs\_timestamps.cpp`) ejecuta el DFS y escribe una *traza* de eventos en JSON
(`enter u`, `exit u`, consultas). La escena de Manim (`animation/escena.py`) lee esa
traza y anima cada evento. Si se cambia el árbol de entrada, cambia la animación.

## Base del código

La implementación en C++ parte del **código de clase del Prof. Víctor Racsó Galván Oyola**
(CS2023, UTEC): DFS con `in`/`out`, `is\_ancestor` y lectura de entrada. El grupo le agregó
el **modo `--trace`**, que registra cada evento del DFS (`enter`/`exit`) y emite la traza JSON,
además de toda la animación en Manim, los casos de prueba y el informe.

## Contenido del video

1. Título e integrantes
2. Introducción conceptual (qué son `tin`/`tout` y para qué sirven)
3. Demostración animada sobre un árbol de 7 nodos + consultas `es\_ancestro`
4. Intervalos `\[tin, tout]` anidados
5. Casos borde: un solo nodo y cadena (peor caso de profundidad)
6. Análisis de complejidad y créditos

## Estructura del repositorio

```
cpp/dfs\_timestamps.cpp   implementación real del DFS con tin/tout + generador de traza
data/                    árboles de entrada (caso principal y casos borde)
animation/escena.py      escena de Manim que consume las trazas
scripts/run\_all.py       compila, genera trazas y renderiza el video
```

## Requisitos

* `g++` con soporte C++17
* Python 3.10+
* [Manim Community](https://docs.manim.community/en/stable/installation.html)
(`pip install -r animation/requirements.txt`) y FFmpeg
* (La escena usa solo `Text`, no requiere LaTeX)

## Cómo ejecutar

```bash
git clone https://github.com/elmano777/proyecto2-aed.git
cd proyecto2-aed
pip install -r animation/requirements.txt
python scripts/run\_all.py        # 1080p. Usa "python scripts/run\_all.py l" para una prueba rápida
```

El video queda en `media/videos/escena/<calidad>/DFSTimestamps.mp4`.

Para probar solo el C++ con otro árbol:

```bash
g++ -O2 -std=c++17 cpp/dfs\_timestamps.cpp -o dfs\_timestamps
./dfs\_timestamps < data/arbol\_ejemplo.txt           # SI / NO por consulta
./dfs\_timestamps --trace < data/arbol\_ejemplo.txt   # traza JSON para la animación
```

Formato de entrada: `n q`, luego `n-1` aristas (`u v`, nodos 1..n, raíz 1),
luego `q` consultas `u v` ("¿u es ancestro de v?").

## Complejidad

|Operación|Tiempo|Memoria|
|-|-|-|
|Construcción de `tin`/`tout` (DFS)|O(n)|O(n)|
|`es\_ancestro(u, v)`|O(1)|—|

## Video

Enlace: *(pegar aquí el enlace del video)*

## Referencias

* Manim Community Documentation: https://docs.manim.community/
* Código de clase del Prof. Víctor Racsó Galván Oyola (CS2023, UTEC), base del DFS con tin/tout
* Canal 3Blue1Brown (inspiración de estilo): https://www.3blue1brown.com/

