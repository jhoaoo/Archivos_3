
from __future__ import annotations
from pathlib import Path
import re, pandas as pd

class AppError(Exception): ...

class Contador:
    def __init__(self, archivo: Path):
        self.archivo = archivo

    def _leer(self) -> int:
        if not self.archivo.exists():
            self.archivo.write_text("0", encoding="utf-8")
            return 0
        s = self.archivo.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"^-?\d+$", s):
            self.archivo.write_text("0", encoding="utf-8")
            return 0
        return int(s)

    def _escribir(self, n: int) -> None:
        tmp = self.archivo.with_suffix(".tmp")
        tmp.write_text(str(n), encoding="utf-8")
        tmp.replace(self.archivo)

    def inc(self) -> int:
        n = self._leer() + 1
        self._escribir(n)
        return n

    def dec(self) -> int:
        n = self._leer() - 1
        self._escribir(n)
        return n

    def ver(self) -> int:
        return self._leer()

def pedir_archivo() -> Path:
    while True:
        ruta = Path(input("Archivo para el contador [contador.txt]: ").strip() or "contador.txt")
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            if not ruta.exists(): ruta.write_text("0", encoding="utf-8")
            return ruta
        except Exception as e:
            print(f"[!] {e}\n")

def menu():
    print("=== Contador Persistente ===")
    ruta = pedir_archivo()
    c = Contador(ruta)
    # Muestra con pandas una tabla simple del valor actual
    df = pd.DataFrame([{"archivo": str(ruta), "valor_actual": c.ver()}])
    print(df.to_string(index=False))
    while True:
        print("\n1) Ver  2) Incrementar  3) Decrementar  4) Salir")
        op = input("Opción: ").strip()
        if op not in {"1","2","3","4"}:
            print("[!] Opción inválida"); continue
        if op=="1": print("Valor:", c.ver())
        elif op=="2": print("Nuevo valor:", c.inc())
        elif op=="3": print("Nuevo valor:", c.dec())
        else: break

if __name__ == "__main__":
    menu()
