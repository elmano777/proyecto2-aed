"""
Animación de DFS Timestamps (tin / tout) con Manim Community.

La animación NO está hecha "a mano": lee las trazas JSON que genera la
implementación en C++ (cpp/dfs_timestamps.cpp, basada en el código de clase). Si cambias el árbol de entrada,
cambia la animación.

Render:  manim -qh animation/escena.py DFSTimestamps
(o usa:  python scripts/run_all.py)
"""
import json
from pathlib import Path

from manim import *

# ----------------------------------------------------------------------------
# EDITA ESTO: datos del grupo para la intro / créditos
# ----------------------------------------------------------------------------
TITULO_PROYECTO = "DFS Timestamps: tin y tout"
INTEGRANTES = ["Fernando Aguirre Milla, Rolando David Diaz Jara, Eliseo David Velasquez Diaz"]
CURSO = "CS2023 - Algoritmos y Estructuras de Datos (2026-2)"
# ----------------------------------------------------------------------------

TRACES = Path(__file__).resolve().parent.parent / "traces"

COLOR_ENTRADA = YELLOW   # nodo "abierto" (en la pila del DFS)
COLOR_SALIDA = GREEN     # nodo terminado
COLOR_BASE = LIGHT_GRAY


def cargar(nombre):
    with open(TRACES / f"{nombre}.json", encoding="utf-8") as f:
        return json.load(f)


class DFSTimestamps(Scene):
    def construct(self):
        self.intro()
        self.concepto()
        self.run_dfs("arbol_ejemplo", "Demostración: árbol de 7 nodos",
                     con_intervalos=True)
        self.tarjeta("Caso borde 1: un solo nodo")
        self.run_dfs("caso_un_nodo", "Un solo nodo: tin = 1, tout = 2")
        self.tarjeta("Caso borde 2: cadena (peor caso de profundidad)")
        self.run_dfs("caso_cadena", "Cadena de 5 nodos: profundidad n")
        self.complejidad()
        self.creditos()

    # ------------------------------------------------------------------ utils
    def limpiar(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects])

    def tarjeta(self, texto):
        t = Text(texto, font_size=36)
        self.play(Write(t))
        self.wait(1)
        self.play(FadeOut(t))

    # ------------------------------------------------------------------ intro
    def intro(self):
        titulo = Text(TITULO_PROYECTO, font_size=44)
        sub = Text(CURSO, font_size=22, color=GRAY_B).next_to(titulo, DOWN)
        autores = Text(", ".join(INTEGRANTES), font_size=24).next_to(sub, DOWN, buff=0.5)
        self.play(Write(titulo))
        self.play(FadeIn(sub), FadeIn(autores))
        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(sub), FadeOut(autores))

    def concepto(self):
        t1 = Text("¿Qué son tin y tout?", font_size=38).to_edge(UP)
        lineas = VGroup(
            Text("En un DFS, cada nodo recibe dos tiempos:", font_size=28),
            Text("tin  = cuando se descubre el nodo", font_size=28, color=COLOR_ENTRADA),
            Text("tout = cuando se terminan de visitar sus descendientes",
                 font_size=28, color=COLOR_SALIDA),
            Text("u es ancestro de v  <=>  tin[u] ≤ tin[v]  y  tout[v] ≤ tout[u]",
                 font_size=28),
            Text("Se verifica en O(1) tras un solo DFS en O(n).", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(t1, DOWN, buff=0.6)
        self.play(Write(t1))
        for l in lineas:
            self.play(FadeIn(l, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.8)
        usos = Text("Usos: ancestros, subárboles, LCA, Euler tour, consultas en árboles",
                    font_size=22, color=GRAY_B).to_edge(DOWN)
        self.play(FadeIn(usos))
        self.wait(2)
        self.limpiar()

    # ------------------------------------------------------------- demo (DFS)
    def construir_grafo(self, n, edges):
        nodos = list(range(1, n + 1))          # nodos 1..n, raíz 1 (como en el código de clase)
        etiquetas = {i: Text(str(i), font_size=26, color=BLACK) for i in nodos}
        cfg = {"radius": 0.3, "color": COLOR_BASE}
        if n == 1:
            return Graph([1], [], layout={1: ORIGIN}, labels=etiquetas,
                         vertex_config=cfg)
        g = Graph(nodos, edges, layout="tree",
                  layout_config={"root_vertex": 1}, labels=etiquetas,
                  vertex_config=cfg)
        if g.height > 4.2:
            g.scale_to_fit_height(4.2)
        return g

    def run_dfs(self, nombre, titulo, con_intervalos=False):
        data = cargar(nombre)
        n = data["n"]
        g = self.construir_grafo(n, [tuple(e) for e in data["edges"]])
        g.move_to(DOWN * 0.2)

        enc = Text(titulo, font_size=30).to_edge(UP)
        reloj = Text("t = 0", font_size=28, color=WHITE).to_corner(UR)
        self.play(FadeIn(enc), FadeIn(reloj), Create(g))

        tin, tout = {}, {}
        rotulos = {}
        for ev in data["events"]:
            u, t = ev["u"], ev["t"]
            nuevo_reloj = Text(f"t = {t}", font_size=28).align_to(reloj, RIGHT) \
                                                          .align_to(reloj, UP)
            if ev["type"] == "enter":
                tin[u] = t
                r = Text(f"[{t}, ?]", font_size=20, color=COLOR_ENTRADA)
                r.next_to(g.vertices[u], DOWN, buff=0.1)
                rotulos[u] = r
                self.play(g.vertices[u].animate.set_color(COLOR_ENTRADA),
                          FadeIn(r), Transform(reloj, nuevo_reloj), run_time=0.5)
            else:
                tout[u] = t
                nuevo = Text(f"[{tin[u]}, {t}]", font_size=20, color=COLOR_SALIDA)
                nuevo.move_to(rotulos[u])
                self.play(g.vertices[u].animate.set_color(COLOR_SALIDA),
                          Transform(rotulos[u], nuevo),
                          Transform(reloj, nuevo_reloj), run_time=0.5)
        self.wait(0.5)

        # Consultas es_ancestro(u, v) en O(1): solo comparan enteros ya calculados
        for q in data["queries"]:
            u, v, res = q["u"], q["v"], q["result"]
            self.play(g.vertices[u].animate.set_color(ORANGE),
                      g.vertices[v].animate.set_color(PINK), run_time=0.4)
            l1 = Text(f"tin[{u}]={tin[u]} ≤ tin[{v}]={tin[v]}   y   "
                      f"tout[{v}]={tout[v]} ≤ tout[{u}]={tout[u]}", font_size=24)
            l2 = Text(f"es_ancestro({u}, {v}) = {'verdadero' if res else 'falso'}",
                      font_size=30, color=GREEN if res else RED)
            msg = VGroup(l1, l2).arrange(DOWN, buff=0.2).to_edge(DOWN)
            self.play(Write(msg))
            self.wait(1.5)
            self.play(FadeOut(msg),
                      g.vertices[u].animate.set_color(COLOR_SALIDA),
                      g.vertices[v].animate.set_color(COLOR_SALIDA), run_time=0.4)

        if con_intervalos:
            self.limpiar()
            self.mostrar_intervalos(n, tin, tout)
        self.limpiar()

    # -------------------------------------------------------- intervalos nested
    def mostrar_intervalos(self, n, tin, tout):
        enc = Text("Cada nodo es un intervalo [tin, tout]", font_size=30).to_edge(UP)
        self.play(Write(enc))
        X = lambda t: -4 + 8 * (t - 1) / (2 * n - 1)   # tiempos van de 1 a 2n
        orden = sorted(range(1, n + 1), key=lambda u: tin[u])
        barras = []
        for i, u in enumerate(orden):
            y = 2.0 - i * 0.55
            barra = Line([X(tin[u]), y, 0], [X(tout[u]), y, 0],
                         stroke_width=10, color=COLOR_SALIDA)
            nombre = Text(f"nodo {u}", font_size=20).move_to([-5.3, y, 0])
            a = Text(str(tin[u]), font_size=16).next_to(barra.get_start(), LEFT, buff=0.08)
            b = Text(str(tout[u]), font_size=16).next_to(barra.get_end(), RIGHT, buff=0.08)
            barras.append(VGroup(nombre, barra, a, b))
        self.play(LaggedStart(*[Create(b) for b in barras], lag_ratio=0.2))
        nota = Text("Ancestro  =  intervalo que contiene al otro\n"
                    "Sin relación  =  intervalos disjuntos",
                    font_size=24, color=GRAY_B).to_edge(DOWN)
        self.play(FadeIn(nota))
        self.wait(3)

    # ----------------------------------------------------------- complejidad
    def complejidad(self):
        t = Text("Complejidad", font_size=40).to_edge(UP)
        filas = VGroup(
            Text("Construcción (un DFS):  O(n)", font_size=30),
            Text("Consulta es_ancestro(u, v):  O(1)", font_size=30),
            Text("Memoria (tin y tout):  O(n)", font_size=30),
            Text("Peor caso (cadena): recursión de profundidad n,\n"
                 "en la práctica se usa un DFS iterativo",
                 font_size=24, color=GRAY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(t, DOWN, buff=0.7)
        self.play(Write(t))
        for f in filas:
            self.play(FadeIn(f, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.6)
        self.wait(2)
        self.limpiar()

    # --------------------------------------------------------------- créditos
    def creditos(self):
        t = Text("Créditos", font_size=40).to_edge(UP)
        nombres = VGroup(*[Text(n, font_size=30) for n in INTEGRANTES]) \
            .arrange(DOWN, buff=0.3)
        pie = Text(CURSO, font_size=22, color=GRAY_B).to_edge(DOWN)
        estilo = Text("Estilo inspirado en 3Blue1Brown · Hecho con Manim Community",
                      font_size=20, color=GRAY_B).next_to(pie, UP)
        self.play(Write(t), FadeIn(nombres), FadeIn(pie), FadeIn(estilo))
        self.wait(3)
