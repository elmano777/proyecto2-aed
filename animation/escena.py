import json
from pathlib import Path

from manim import *

TITULO_PROYECTO = "DFS Timestamps: tin y tout"
INTEGRANTES = ["Aguirre Milla, Fernando",
               "Díaz Jara, Rolando David",
               "Velásquez Díaz, Eliseo David"]
CURSO = "CS2023 - Algoritmos y Estructuras de Datos (2026-2)"

TRACES = Path(__file__).resolve().parent.parent / "traces"

COLOR_ENTRADA = YELLOW
COLOR_SALIDA = GREEN
COLOR_BASE = LIGHT_GRAY


def cargar(nombre):
    with open(TRACES / f"{nombre}.json", encoding="utf-8") as f:
        return json.load(f)


def disponer_arbol(n, edges, raiz=1):
    ady = {i: [] for i in range(1, n + 1)}
    for a, b in edges:
        ady[a].append(b)
        ady[b].append(a)
    padre, prof, hijos = {raiz: 0}, {raiz: 0}, {i: [] for i in range(1, n + 1)}
    cola = [raiz]
    for u in cola:
        for v in ady[u]:
            if v != padre[u]:
                padre[v], prof[v] = u, prof[u] + 1
                hijos[u].append(v)
                cola.append(v)

    x, siguiente_hoja = {}, [0]

    def colocar(u):
        if not hijos[u]:
            x[u] = siguiente_hoja[0]
            siguiente_hoja[0] += 1
        else:
            for h in hijos[u]:
                colocar(h)
            x[u] = (x[hijos[u][0]] + x[hijos[u][-1]]) / 2

    colocar(raiz)
    columnas, filas = siguiente_hoja[0], max(prof.values()) + 1
    pos, lado = {}, {}
    if columnas >= filas:
        gx = min(2.0, 10 / max(columnas - 1, 1))
        gy = min(1.5, 3.6 / max(filas - 1, 1))
        centro = (columnas - 1) / 2
        for u in range(1, n + 1):
            pos[u] = np.array([(x[u] - centro) * gx, ((filas - 1) / 2 - prof[u]) * gy, 0])
            lado[u] = LEFT if x[u] < centro - 1e-9 else RIGHT
    else:
        gx = min(1.7, 10 / max(filas - 1, 1))
        for u in range(1, n + 1):
            pos[u] = np.array([(prof[u] - (filas - 1) / 2) * gx, 0, 0])
            lado[u] = DOWN
    return pos, lado


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

    def limpiar(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects])

    def tarjeta(self, texto):
        t = Text(texto, font_size=36)
        self.play(Write(t))
        self.wait(1)
        self.play(FadeOut(t))

    def intro(self):
        titulo = Text(TITULO_PROYECTO, font_size=44)
        sub = Text(CURSO, font_size=22, color=GRAY_B).next_to(titulo, DOWN)
        autores = VGroup(*[Text(nombre, font_size=26) for nombre in INTEGRANTES]) \
            .arrange(DOWN, buff=0.2).next_to(sub, DOWN, buff=0.5)
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

    def construir_grafo(self, n, edges):
        nodos = list(range(1, n + 1))
        pos, lado = disponer_arbol(n, edges)
        cfg = {"radius": 0.3, "color": COLOR_BASE}
        g = Graph(nodos, edges, layout=pos, vertex_config=cfg)
        return g, lado

    def run_dfs(self, nombre, titulo, con_intervalos=False):
        data = cargar(nombre)
        n = data["n"]
        g, lado = self.construir_grafo(n, [tuple(e) for e in data["edges"]])
        g.move_to(DOWN * 0.2)
        numeros = VGroup(*[Text(str(u), font_size=26, color=BLACK).move_to(g.vertices[u])
                           for u in range(1, n + 1)])

        enc = Text(titulo, font_size=30).to_edge(UP)
        reloj = Text("t = 0", font_size=28, color=WHITE).to_corner(UR)
        self.play(FadeIn(enc), FadeIn(reloj), Create(g), FadeIn(numeros))

        tin, tout = {}, {}
        rotulos = {}
        for ev in data["events"]:
            u, t = ev["u"], ev["t"]
            nuevo_reloj = Text(f"t = {t}", font_size=28).align_to(reloj, RIGHT) \
                .align_to(reloj, UP)
            if ev["type"] == "enter":
                tin[u] = t
                r = Text(f"[{t}, ?]", font_size=20, color=COLOR_ENTRADA)
                r.next_to(g.vertices[u], lado[u], buff=0.12)
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

        for q in data["queries"]:
            u, v, res = q["u"], q["v"], q["result"]
            self.play(g.vertices[u].animate.set_color(ORANGE),
                      g.vertices[v].animate.set_color(PINK), run_time=0.4)
            l1 = Text(f"tin[{u}]={tin[u]} ≤ tin[{v}]={tin[v]}   y   "
                      f"tout[{v}]={tout[v]} ≤ tout[{u}]={tout[u]}", font_size=24)
            l2 = Text(f"es_ancestro({u}, {v}) = {'verdadero' if res else 'falso'}",
                      font_size=30, color=GREEN if res else RED)
            msg = VGroup(l1, l2).arrange(DOWN, buff=0.2).to_edge(DOWN)
            self.play(FadeIn(msg, shift=UP * 0.2))
            self.wait(1.5)
            self.play(FadeOut(msg),
                      g.vertices[u].animate.set_color(COLOR_SALIDA),
                      g.vertices[v].animate.set_color(COLOR_SALIDA), run_time=0.4)

        if con_intervalos:
            self.limpiar()
            self.mostrar_intervalos(n, tin, tout)
        self.limpiar()

    def mostrar_intervalos(self, n, tin, tout):
        enc = Text("Cada nodo es un intervalo [tin, tout]", font_size=30).to_edge(UP)
        self.play(Write(enc))
        X = lambda t: -4 + 8 * (t - 1) / (2 * n - 1)
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

    def complejidad(self):
        t = Text("Complejidad", font_size=40).to_edge(UP)
        filas = VGroup(
            Text("Construcción (un DFS):  O(n)", font_size=30),
            Text("Consulta es_ancestro(u, v):  O(1)", font_size=30),
            Text("Memoria (tin y tout):  O(n)", font_size=30),
            Text("Sin tin/tout: subir por los padres de v cuesta O(h)",
                 font_size=26, color=GRAY_B),
            Text("Peor caso (cadena): profundidad n, por eso el DFS\n"
                 "es iterativo (pila explícita) y no recursivo",
                 font_size=24, color=GRAY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(t, DOWN, buff=0.7)
        self.play(Write(t))
        for f in filas:
            self.play(FadeIn(f, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.6)
        self.wait(2)
        self.limpiar()

    def creditos(self):
        t = Text("Créditos", font_size=40).to_edge(UP)
        nombres = VGroup(*[Text(n, font_size=30) for n in INTEGRANTES]) \
            .arrange(DOWN, buff=0.3)
        pie = Text(CURSO, font_size=22, color=GRAY_B).to_edge(DOWN)
        estilo = Text("Estilo inspirado en 3Blue1Brown · Hecho con Manim Community",
                      font_size=20, color=GRAY_B).next_to(pie, UP)
        self.play(Write(t), FadeIn(nombres), FadeIn(pie), FadeIn(estilo))
        self.wait(3)