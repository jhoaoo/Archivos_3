from __future__ import annotations
import re, pandas as pd
from dataclasses import dataclass
from pathlib import Path

ARCHIVO = Path("estudiantes.txt")

class ErrorDatos(Exception): ...

RX_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{2,50}$")
RX_EDAD = re.compile(r"^\d{1,2}$")
RX_NOTA = re.compile(r"^\d{1,2}(\.\d{1,2})?$")

@dataclass
class Estudiante:
    nombre: str
    edad: int
    calificaciones: list[float]

    @staticmethod
    def crear(nombre: str, edad: str, calif_str: str) -> "Estudiante":
        if not RX_NOMBRE.fullmatch(nombre.strip()): raise ErrorDatos("Nombre inválido")
        if not RX_EDAD.fullmatch(edad) or not (3 <= int(edad) <= 100): raise ErrorDatos("Edad inválida (3-100)")
        partes = [p.strip() for p in calif_str.split(",") if p.strip()]
        if not partes: raise ErrorDatos("Debe ingresar al menos una calificación")
        califs = []
        for p in partes:
            if not RX_NOTA.fullmatch(p): raise ErrorDatos(f"Calificación inválida: {p}")
            v = float(p)
            if v < 0 or v > 20: raise ErrorDatos(f"Calificación fuera de rango: {v}")
            califs.append(v)
        return Estudiante(nombre.strip(), int(edad), califs)

def leer_todo() -> list[Estudiante]:
    if not ARCHIVO.exists(): return []
    ests: list[Estudiante] = []
    for linea in ARCHIVO.read_text(encoding="utf-8").splitlines():
        if not linea.strip(): continue
        try:
            nombre, edad, califs = linea.split("|")
            ests.append(Estudiante.crear(nombre, edad, califs))
        except Exception:
            continue
    return ests

def guardar(e: Estudiante) -> None:
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)
    with ARCHIVO.open("a", encoding="utf-8") as f:
        f.write(f"{e.nombre}|{e.edad}|{','.join(map(lambda x: f'{x:.2f}', e.calificaciones))}\n")

def promedio_de(nombre: str) -> float | None:
    for e in leer_todo():
        if e.nombre.lower() == nombre.lower():
            return round(sum(e.calificaciones)/len(e.calificaciones), 2)
    return None

def mostrar_tabla() -> None:
    ests = leer_todo()
    df = pd.DataFrame([{"nombre": e.nombre, "edad": e.edad, "calificaciones": ",".join(map(str, e.calificaciones))} for e in ests])
    print(df.to_string(index=False) if not df.empty else "(sin registros)")

def menu():
    print("=== REGISTRO DE ESTUDIANTES ===")
    while True:
        print("\n1) Agregar  2) Listar  3) Promedio por nombre  4) Salir")
        op = input("Opción: ").strip()
        if op not in {"1","2","3","4"}:
            print("[!] Opción inválida"); continue
        if op=="1":
            while True:
                try:
                    n = input("Nombre: ").strip()
                    e = input("Edad: ").strip()
                    c = input("Calificaciones separadas por coma (0-20): ").strip()
                    est = Estudiante.crear(n, e, c)
                    guardar(est)
                    print("[OK] Guardado.")
                    break
                except ErrorDatos as ex:
                    print(f"[!] {ex}. Intente nuevamente.\n")
        elif op=="2":
            mostrar_tabla()
        elif op=="3":
            nb = input("Nombre: ").strip()
            p = promedio_de(nb)
            print(f"Promedio: {p}" if p is not None else "No encontrado")
        else:
            break

if __name__ == "__main__":
    menu()
