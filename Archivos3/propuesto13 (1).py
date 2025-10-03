from __future__ import annotations
import re, pandas as pd, csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ARCHIVO = Path("gastos.txt")
RX_TXT = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 .,;:'\"\-]{2,100}$")
RX_MONTO = re.compile(r"^\d+(\.\d{1,2})?$")

@dataclass
class Gasto:
    descripcion: str
    monto: float
    fecha: str  # YYYY-MM-DD
    categoria: str

    @staticmethod
    def crear(desc: str, monto: str, fecha: str, cat: str) -> "Gasto":
        if not RX_TXT.fullmatch(desc.strip()): raise ValueError("Descripción inválida")
        if not RX_MONTO.fullmatch(monto): raise ValueError("Monto inválido")
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Fecha inválida (YYYY-MM-DD)")
        if not RX_TXT.fullmatch(cat.strip()): raise ValueError("Categoría inválida")
        return Gasto(desc.strip(), float(monto), fecha, cat.strip())

def leer_todo() -> list[Gasto]:
    if not ARCHIVO.exists(): return []
    out = []
    for linea in ARCHIVO.read_text(encoding="utf-8").splitlines():
        if not linea.strip(): continue
        try:
            d, m, f, c = linea.split("|")
            out.append(Gasto.crear(d, m, f, c))
        except Exception:
            continue
    return out

def escribir_append(g: Gasto) -> None:
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)
    with ARCHIVO.open("a", encoding="utf-8") as f:
        f.write(f"{g.descripcion}|{g.monto:.2f}|{g.fecha}|{g.categoria}\n")

def resumen():
    gastos = leer_todo()
    if not gastos: print("(sin gastos)"); return
    aggr = {}
    for g in gastos:
        clave = (g.fecha[:7], g.categoria)
        aggr[clave] = aggr.get(clave, 0.0) + g.monto
    df = pd.DataFrame([{"mes": k[0], "categoria": k[1], "total": round(v,2)} for k,v in aggr.items()])
    print(df.sort_values(["mes","categoria"]).to_string(index=False))

def exportar_csv():
    gastos = leer_todo()
    if not gastos: print("(sin gastos)"); return
    with open("gastos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Descripción","Monto","Fecha","Categoría"])
        for g in gastos:
            w.writerow([g.descripcion, f"{g.monto:.2f}", g.fecha, g.categoria])
    print("[OK] Exportado a gastos.csv")

def menu():
    print("=== GASTOS PERSONALES ===")
    while True:
        print("\n1) Registrar  2) Resumen Mes/Categoría  3) Exportar CSV  4) Salir")
        op = input("Opción: ").strip()
        if op not in {"1","2","3","4"}:
            print("[!] Opción inválida"); continue
        if op=="1":
            while True:
                try:
                    d = input("Descripción: ").strip()
                    m = input("Monto: ").strip()
                    f = input("Fecha (YYYY-MM-DD): ").strip()
                    c = input("Categoría: ").strip()
                    escribir_append(Gasto.crear(d,m,f,c)); print("[OK] Registrado."); break
                except Exception as e:
                    print(f"[!] {e}. Intente nuevamente.\n")
        elif op=="2":
            resumen()
        elif op=="3":
            exportar_csv()
        else:
            break

if __name__ == "__main__":
    menu()
