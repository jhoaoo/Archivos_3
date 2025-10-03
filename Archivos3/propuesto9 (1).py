from __future__ import annotations
import re, pandas as pd
from dataclasses import dataclass
from pathlib import Path

class ErrorLibro(Exception): ...

RX_TIT = re.compile(r"^.{2,100}$")
RX_AUT = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ,.]{3,80}$")
RX_ANO = re.compile(r"^\d{4}$")

@dataclass
class Libro:
    titulo: str
    autor: str
    anio: int
    @staticmethod
    def crear(titulo: str, autor: str, anio_s: str) -> "Libro":
        if not RX_TIT.fullmatch(titulo.strip()): raise ErrorLibro("Título inválido")
        if not RX_AUT.fullmatch(autor.strip()): raise ErrorLibro("Autor inválido")
        if not RX_ANO.fullmatch(anio_s): raise ErrorLibro("Año inválido (YYYY)")
        anio = int(anio_s)
        if anio < 1450 or anio > 2100: raise ErrorLibro("Año fuera de rango razonable")
        return Libro(titulo.strip(), autor.strip(), anio)

def main():
    print("=== Registro de Libros ===")
    libros: list[Libro] = []
    while True:
        tit = input("Título (Enter para terminar): ").strip()
        if not tit: break
        aut = input("Autor: ").strip()
        ano = input("Año (YYYY): ").strip()
        try:
            libros.append(Libro.crear(tit, aut, ano))
            print("[OK] Añadido.")
        except ErrorLibro as e:
            print(f"[!] {e}\n"); continue
    df = pd.DataFrame([l.__dict__ for l in libros]) if libros else pd.DataFrame(columns=["titulo","autor","anio"])
    print(df.to_string(index=False))
    ruta = Path(input("Guardar en libros.txt [libros.txt]: ").strip() or "libros.txt")
    ruta.write_text(df.to_string(index=False), encoding="utf-8")
    print(f"[OK] Guardado en {ruta.resolve()}")

if __name__ == "__main__":
    main()
