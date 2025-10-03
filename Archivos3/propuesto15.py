from __future__ import annotations
import re, pandas as pd
from dataclasses import dataclass
from pathlib import Path

ARCHIVO = Path("peliculas.txt")
RX_TXT = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 .,:;'\"\-]{2,100}$")
RX_ANIO = re.compile(r"^(19\\d{2}|20\\d{2}|2025)$")

@dataclass
class Pelicula:
    titulo: str
    director: str
    anio: int

    @staticmethod
    def crear(titulo: str, director: str, anio: str) -> "Pelicula":
        if not RX_TXT.fullmatch(titulo.strip()): raise ValueError("Título inválido")
        if not RX_TXT.fullmatch(director.strip()): raise ValueError("Director inválido")
        if not RX_ANIO.fullmatch(anio): raise ValueError("Año inválido (1900-2025)")
        return Pelicula(titulo.strip(), director.strip(), int(anio))

def leer_todo() -> list[Pelicula]:
    if not ARCHIVO.exists(): return []
    out = []
    for linea in ARCHIVO.read_text(encoding="utf-8").splitlines():
        if not linea.strip(): continue
        try:
            t, d, a = linea.split("|")
            out.append(Pelicula.crear(t,d,a))
        except Exception:
            continue
    return out

def escribir_append(p: Pelicula) -> None:
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)
    with ARCHIVO.open("a", encoding="utf-8") as f:
        f.write(f"{p.titulo}|{p.director}|{p.anio}\n")

def buscar(campo: str, texto: str) -> list[Pelicula]:
    texto = texto.lower()
    if campo == "t": return [p for p in leer_todo() if texto in p.titulo.lower()]
    if campo == "d": return [p for p in leer_todo() if texto in p.director.lower()]
    return []

def listar():
    pelis = leer_todo()
    df = pd.DataFrame([p.__dict__ for p in pelis])
    print(df.to_string(index=False) if not df.empty else "(sin registros)")

def menu():
    print("=== REGISTRO DE PELÍCULAS ===")
    while True:
        print("\n1) Agregar  2) Buscar  3) Listar  4) Salir")
        op = input("Opción: ").strip()
        if op not in {"1","2","3","4"}:
            print("[!] Opción inválida"); continue
        if op=="1":
            while True:
                try:
                    t = input("Título: ").strip()
                    d = input("Director: ").strip()
                    a = input("Año (1900-2025): ").strip()
                    escribir_append(Pelicula.crear(t,d,a)); print("[OK] Registrada."); break
                except Exception as e:
                    print(f"[!] {e}. Intente nuevamente.\n")
        elif op=="2":
            campo = input("Buscar por (t)ítulo o (d)irector: ").strip().lower()
            if campo not in {"t","d"}: print("[!] Campo inválido"); continue
            txt = input("Texto: ").strip()
            res = buscar(campo, txt)
            df = pd.DataFrame([p.__dict__ for p in res])
            print(df.to_string(index=False) if not df.empty else "Sin coincidencias")
        elif op=="3":
            listar()
        else:
            break

if __name__ == "__main__":
    menu()
