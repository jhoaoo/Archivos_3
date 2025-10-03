
from __future__ import annotations
import re, pandas as pd
from dataclasses import dataclass
from pathlib import Path

class ErrorDatos(Exception): ...

RX_NOM = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{2,60}$")
RX_NUM = re.compile(r"^\d+(\.\d{1,2})?$")

@dataclass
class Empleado:
    nombre: str
    salario: float
    @staticmethod
    def crear(nombre: str, salario_s: str) -> "Empleado":
        if not RX_NOM.fullmatch(nombre.strip()):
            raise ErrorDatos("Nombre inválido")
        if not RX_NUM.fullmatch(salario_s):
            raise ErrorDatos("Salario inválido (número con hasta 2 decimales)")
        salario = float(salario_s)
        if salario<=0: raise ErrorDatos("Salario debe ser > 0")
        return Empleado(nombre.strip(), salario)

class GrupoEmpleados:
    def __init__(self): self.items: list[Empleado]=[]
    def agregar(self, e: Empleado): self.items.append(e)
    def promedio(self) -> float:
        return round(sum(e.salario for e in self.items)/len(self.items), 2) if self.items else 0.0
    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([e.__dict__ for e in self.items]) if self.items else pd.DataFrame(columns=["nombre","salario"])

def main():
    print("=== GrupoEmpleados ===")
    grupo = GrupoEmpleados()
    while True:
        nombre = input("Nombre (Enter para terminar): ").strip()
        if not nombre: break
        salario = input("Salario: ").strip()
        try:
            grupo.agregar(Empleado.crear(nombre, salario))
            print("[OK] Añadido.")
        except ErrorDatos as e:
            print(f"[!] {e}\n"); continue
    df = grupo.to_frame()
    print(df.to_string(index=False))
    print("Salario promedio:", grupo.promedio())
    out = Path(input("Guardar planilla .txt [empleados.txt]: ").strip() or "empleados.txt")
    out.write_text(df.to_string(index=False), encoding="utf-8")
    print(f"[OK] Guardado en {out.resolve()}")

if __name__ == "__main__":
    main()
