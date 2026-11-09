import json
import random
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXE = RAIZ / ("dfs_timestamps_test.exe" if sys.platform.startswith("win") else "dfs_timestamps_test")


def correr(entrada, *args):
    return subprocess.run([str(EXE), *args], input=entrada, capture_output=True, text=True, check=True).stdout


def entrada_de(n, aristas, consultas):
    return (f"{n} {len(consultas)}\n" + "".join(f"{a} {b}\n" for a, b in aristas)
            + "".join(f"{u} {v}\n" for u, v in consultas))


def arbol_aleatorio(n):
    etiquetas = [1] + random.sample(range(2, n + 1), n - 1) if n > 1 else [1]
    padre = {1: None}
    aristas = []
    for i in range(1, n):
        p = etiquetas[random.randrange(i)]
        padre[etiquetas[i]] = p
        aristas.append((p, etiquetas[i]) if random.random() < 0.5 else (etiquetas[i], p))
    random.shuffle(aristas)
    return padre, aristas


def es_ancestro_bruto(padre, u, v):
    while v is not None:
        if v == u:
            return True
        v = padre[v]
    return False


def main():
    subprocess.run(["g++", "-O2", "-std=c++17", str(RAIZ / "cpp/dfs_timestamps.cpp"), "-o", str(EXE)], check=True)
    fallos = 0

    esperado = {"arbol_ejemplo": ["SI", "NO", "SI"], "caso_un_nodo": ["SI"], "caso_cadena": ["SI", "NO"]}
    for caso, res in esperado.items():
        obtenido = correr((RAIZ / "data" / f"{caso}.txt").read_text()).split()
        ok = obtenido == res
        fallos += not ok
        print(f"[{'ok' if ok else 'FALLO'}] data/{caso}.txt -> {obtenido}")

    random.seed(2023)
    for _ in range(2000):
        n = random.randint(1, 40)
        padre, aristas = arbol_aleatorio(n)
        consultas = [(random.randint(1, n), random.randint(1, n)) for _ in range(30)]
        entrada = entrada_de(n, aristas, consultas)
        respuestas = correr(entrada).split()
        if respuestas != ["SI" if es_ancestro_bruto(padre, u, v) else "NO" for u, v in consultas]:
            fallos += 1
        traza = json.loads(correr(entrada, "--trace"))
        tiempos = sorted(e["t"] for e in traza["events"])
        tin = {e["u"]: e["t"] for e in traza["events"] if e["type"] == "enter"}
        tout = {e["u"]: e["t"] for e in traza["events"] if e["type"] == "exit"}
        if tiempos != list(range(1, 2 * n + 1)) or any(tin[v] >= tout[v] for v in tin):
            fallos += 1
    print(f"[{'ok' if not fallos else 'FALLO'}] 2000 árboles aleatorios contra fuerza bruta")

    n = 200000
    entrada = entrada_de(n, [(i, i + 1) for i in range(1, n)], [(1, n), (n, 1)])
    ok = correr(entrada).split() == ["SI", "NO"]
    fallos += not ok
    print(f"[{'ok' if ok else 'FALLO'}] cadena de {n} nodos")

    EXE.unlink(missing_ok=True)
    print("TODAS LAS PRUEBAS PASARON" if not fallos else f"{fallos} FALLOS")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()