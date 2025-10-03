from __future__ import annotations
import re, pandas as pd
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ARCHIVO = Path("tareas.txt")
RX_TXT = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 .,;:'\"\-]{2,100}$")

@dataclass
class Tarea:
    descripcion: str
    vencimiento: str  # YYYY-MM-DD
    estado: str = "Pendiente"

    @staticmethod
    def crear(desc: str, venc: str) -> "Tarea":
        if not RX_TXT.fullmatch(desc.strip()): raise ValueError("Descripción inválida")
        try:
            datetime.strptime(venc, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Fecha inválida (YYYY-MM-DD)")
        return Tarea(desc.strip(), venc)

def leer_todo() -> list[Tarea]:
    if not ARCHIVO.exists(): return []
    out = []
    for linea in ARCHIVO.read_text(encoding="utf-8").splitlines():
        if not linea.strip(): continue
        try:
            d, v, s = linea.split("|")
            out.append(Tarea(d, v, s))
        except ValueError:
            continue
    return out

def escribir_todo(lst: list[Tarea]) -> None:
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)
    with ARCHIVO.open("w", encoding="utf-8") as f:
        for t in lst:
            f.write(f"{t.descripcion}|{t.vencimiento}|{t.estado}\n")

def agregar():
    while True:
        try:
            d = input("Descripción: ").strip()
            v = input("Vence (YYYY-MM-DD): ").strip()
            t = Tarea.crear(d, v)
            tareas = leer_todo(); tareas.append(t); escribir_todo(tareas)
            print("[OK] Tarea agregada."); break
        except Exception as e:
            print(f"[!] {e}. Intente nuevamente.\n")

def completar():
    tareas = leer_todo()
    if not tareas: print("(sin tareas)"); return
    df = pd.DataFrame([{"#": i+1, "descripcion": t.descripcion, "vence": t.vencimiento, "estado": t.estado} for i,t in enumerate(tareas)])
    print(df.to_string(index=False))
    while True:
        idx = input("Número a completar: ").strip()
        if not idx.isdigit() or not (1 <= int(idx) <= len(tareas)):
            print("[!] Número inválido"); continue
        tareas[int(idx)-1].estado = "Completada"
        escribir_todo(tareas)
        print("[OK] Marcada como completada.")
        break

def listar_pendientes():
    pend = [t for t in leer_todo() if t.estado == "Pendiente"]
    df = pd.DataFrame([{"descripcion": t.descripcion, "vence": t.vencimiento, "estado": t.estado} for t in pend])
    print(df.to_string(index=False) if not df.empty else "(sin pendientes)")

def menu():
    print("=== GESTOR DE TAREAS ===")
    while True:
        print("\n1) Agregar  2) Completar  3) Pendientes  4) Salir")
        op = input("Opción: ").strip()
        if op not in {"1","2","3","4"}:
            print("[!] Opción inválida"); continue
        if op=="1": agregar()
        elif op=="2": completar()
        elif op=="3": listar_pendientes()
        else: break

if __name__ == "__main__":
    menu()
