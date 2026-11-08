#!/usr/bin/env python3
"""Compila el C++, genera las trazas JSON y renderiza el video con Manim.

Uso (desde la raíz del repo):   python scripts/run_all.py [calidad]
calidad: l (480p, rápido para probar), m, h (1080p, por defecto), k (4K)
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CASOS = ["arbol_ejemplo", "caso_un_nodo", "caso_cadena"]
calidad = sys.argv[1] if len(sys.argv) > 1 else "h"

exe = RAIZ / ("dfs_timestamps.exe" if sys.platform.startswith("win") else "dfs_timestamps")
subprocess.run(["g++", "-O2", "-std=c++17", str(RAIZ / "cpp/dfs_timestamps.cpp"),
                "-o", str(exe)], check=True)

(RAIZ / "traces").mkdir(exist_ok=True)
for caso in CASOS:
    with open(RAIZ / "data" / f"{caso}.txt") as entrada, \
         open(RAIZ / "traces" / f"{caso}.json", "w") as salida:
        subprocess.run([str(exe), "--trace"], stdin=entrada, stdout=salida, check=True)
    print(f"traza generada: traces/{caso}.json")

subprocess.run([sys.executable, "-m", "manim", f"-q{calidad}",
                str(RAIZ / "animation/escena.py"), "DFSTimestamps"], check=True)
print("Listo. El video está en media/videos/escena/")
