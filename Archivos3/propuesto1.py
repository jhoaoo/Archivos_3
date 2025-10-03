from __future__ import annotations
import re, pandas as pd
from pathlib import Path

class ErrorNumero(Exception): ...
class ErrorArchivo(Exception): ...

class TablaMultiplicar:
    def __init__(self, numero: int):
        if not (1 <= numero <= 10):
            raise ErrorNumero("El número debe estar en el rango de 1 a 10")
        self.numero = numero
        self.resultados: list[tuple[int,int]] = []

    def generar(self) -> None:
        self.resultados = [(i, i*self.numero) for i in range(1, 13)]

    def guardar(self, ruta: Path) -> None:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with ruta.open("w", encoding="utf-8") as f:
                f.write(f"=== Tabla del {self.numero} ===\n")
                for i, r in self.resultados:
                    f.write(f"{i} x {self.numero} = {r}\n")
        except Exception as e:
            raise ErrorArchivo(f"No se pudo guardar el archivo: {e}")

    def mostrar(self) -> None:
        df = pd.DataFrame([{"n":i, f"{i}x{self.numero}":r} for i, r in self.resultados])
        print(df.to_string(index=False))


def pedir_numero() -> int:
    while True:
        s = input("Ingrese un número entero (1-10): ").strip()
        if not re.fullmatch(r"^\d{1,2}$", s):
            print("[!] Entrada inválida, solo enteros"); continue
        n = int(s)
        if not (1 <= n <= 10):
            print("[!] Debe estar entre 1 y 10"); continue
        return n

def pedir_salida(num: int) -> Path:
    nombre = f"tabla_propuesto{num}.txt"
    s = input(f"Nombre de archivo de salida [{nombre}]: ").strip()
    return Path(s or nombre)

def main():
    print("=== TABLA DE MULTIPLICAR ===")
    n = pedir_numero()
    tabla = TablaMultiplicar(n)
    tabla.generar()
    tabla.mostrar()
    ruta = pedir_salida(n)
    try:
        tabla.guardar(ruta)
        print(f"[OK] Guardado en {ruta.resolve()}")
    except ErrorArchivo as e:
        print(f"[!] {e}")

if __name__ == "__main__":
    main()