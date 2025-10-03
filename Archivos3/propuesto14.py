from __future__ import annotations
import re, pandas as pd
from dataclasses import dataclass
from pathlib import Path

ARCHIVO = Path("reservas.txt")
RX_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{2,50}$")
RX_NUM = re.compile(r"^\d+$")

@dataclass
class Habitacion:
    numero: int
    tipo: str
    precio: float

HABITACIONES = [
    Habitacion(101, "Simple", 80.0),
    Habitacion(102, "Simple", 80.0),
    Habitacion(201, "Doble", 120.0),
    Habitacion(202, "Doble", 120.0),
    Habitacion(301, "Suite", 250.0),
]

def leer_reservas() -> list[tuple[str,int,int,float]]:
    if not ARCHIVO.exists(): return []
    out = []
    for linea in ARCHIVO.read_text(encoding="utf-8").splitlines():
        if not linea.strip(): continue
        try:
            cliente, num, noches, total = linea.split("|")
            out.append((cliente, int(num), int(noches), float(total)))
        except Exception:
            continue
    return out

def escribir_reserva(cliente: str, num: int, noches: int, total: float) -> None:
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)
    with ARCHIVO.open("a", encoding="utf-8") as f:
        f.write(f"{cliente}|{num}|{noches}|{total:.2f}\n")

def disponible(num: int) -> bool:
    return all(r[1] != num for r in leer_reservas())

def mostrar_disponibilidad():
    df = pd.DataFrame([{"hab": h.numero, "tipo": h.tipo, "precio": h.precio, "estado": "Disponible" if disponible(h.numero) else "Ocupada"} for h in HABITACIONES])
    print(df.to_string(index=False))

def reservar():
    while True:
        nombre = input("Cliente: ").strip()
        if not RX_NOMBRE.fullmatch(nombre): print("[!] Nombre inválido"); continue
        mostrar_disponibilidad()
        num = input("Número de habitación: ").strip()
        if not RX_NUM.fullmatch(num): print("[!] Número inválido"); continue
        num = int(num)
        hab = next((h for h in HABITACIONES if h.numero==num), None)
        if not hab: print("[!] Habitación no existe"); continue
        if not disponible(num): print("[!] Ya reservada"); continue
        noches = input("Noches: ").strip()
        if not RX_NUM.fullmatch(noches) or int(noches)<=0: print("[!] Noches inválidas"); continue
        noches = int(noches)
        total = hab.precio * noches
        escribir_reserva(nombre, num, noches, total)
        print(f"[OK] Reserva registrada. Total: S/ {total:.2f}")
        break

def factura():
    nombre = input("Cliente para factura: ").strip()
    if not RX_NOMBRE.fullmatch(nombre): print("[!] Nombre inválido"); return
    res = [r for r in leer_reservas() if r[0].lower()==nombre.lower()]
    if not res: print("(sin reservas)"); return
    df = pd.DataFrame([{"hab": n, "noches": k, "subtotal": t} for _,n,k,t in res])
    print(df.to_string(index=False))
    print("TOTAL:", round(df["subtotal"].sum(),2))

def menu():
    print("=== RESERVAS HOTEL ===")
    while True:
        print("\n1) Reservar  2) Disponibilidad  3) Factura  4) Salir")
        op = input("Opción: ").strip()
        if op not in {"1","2","3","4"}: print("[!] Opción inválida"); continue
        if op=="1": reservar()
        elif op=="2": mostrar_disponibilidad()
        elif op=="3": factura()
        else: break

if __name__ == "__main__":
    menu()
