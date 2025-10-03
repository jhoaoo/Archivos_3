
from __future__ import annotations
import re, pickle
from dataclasses import dataclass
from pathlib import Path
import pandas as pd

class AppError(Exception): ...
class ErrorValidacion(AppError): ...

RX_ID = re.compile(r"^\d+$")
RX_CEL = re.compile(r"^\d{9}$")
RX_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{2,60}$")
RX_FECHA = re.compile(r"^\d{2}/\d{2}/\d{4}$")

@dataclass(frozen=True)
class Persona:
    id: int
    nombre: str
    apellido: str
    celular: str
    fecha_nac: str

    @staticmethod
    def validar(id_s: str, nombre: str, apellido: str, celular: str, fecha: str, idx: int) -> "Persona":
        if not RX_ID.fullmatch(id_s): raise ErrorValidacion(f"L{idx}: id inválido")
        if not RX_NOMBRE.fullmatch(nombre.strip()): raise ErrorValidacion(f"L{idx}: nombre inválido")
        if not RX_NOMBRE.fullmatch(apellido.strip()): raise ErrorValidacion(f"L{idx}: apellido inválido")
        if not RX_CEL.fullmatch(celular): raise ErrorValidacion(f"L{idx}: celular(9 dígitos)")
        if not RX_FECHA.fullmatch(fecha): raise ErrorValidacion(f"L{idx}: fecha DD/MM/AAAA")
        return Persona(int(id_s), nombre.strip(), apellido.strip(), celular, fecha)

class Directorio:
    def __init__(self):
        self.validos: list[Persona] = []
        self.invalidos: list[tuple[str,str]] = []

    def cargar_txt(self, ruta: Path) -> None:
        self.validos.clear(); self.invalidos.clear()
        with ruta.open("r", encoding="utf-8") as f:
            for i, linea in enumerate(f, 1):
                linea = linea.strip()
                if not linea: continue
                partes = [p.strip() for p in linea.split(";")]
                if len(partes)!=5:
                    self.invalidos.append((linea, f"L{i}: 5 campos esperados"))
                    continue
                try:
                    self.validos.append(Persona.validar(*partes, idx=i))
                except ErrorValidacion as e:
                    self.invalidos.append((linea, str(e)))

    def guardar_pkl(self, ruta: Path) -> None:
        with ruta.open("wb") as fb:
            pickle.dump(self.validos, fb, protocol=pickle.HIGHEST_PROTOCOL)

    def menu(self) -> None:
        print("=== Directorio de Personas ===")
        # pedir ruta con reintento
        while True:
            ruta_s = input("Ruta .txt (id;nombre;apellido;celular;dd/mm/aaaa): ").strip().strip('"').strip("'")
            ruta = Path(ruta_s)
            try:
                if ruta.suffix.lower()!=".txt": raise AppError("Extensión debe ser .txt")
                if not ruta.exists(): raise AppError("No existe el archivo")
                ruta.read_text(encoding="utf-8")  # prueba
                break
            except Exception as e:
                print(f"[!] {e}. Intente nuevamente.\n")

        self.cargar_txt(ruta)

        # Mostrar con pandas
        if self.validos:
            df_ok = pd.DataFrame([v.__dict__ for v in self.validos])
            print("\n--- REGISTROS VÁLIDOS ---")
            print(df_ok.to_string(index=False))
        else:
            print("\n( Sin registros válidos )")

        if self.invalidos:
            df_bad = pd.DataFrame(self.invalidos, columns=["linea","error"])
            print("\n--- DESCARTES ---")
            print(df_bad.to_string(index=False))

        # Guardar PKL con reintento
        while True:
            out_s = input("Guardar válidos en .pkl [directorio.pkl]: ").strip() or "directorio.pkl"
            out = Path(out_s)
            if out.suffix.lower()!=".pkl":
                print("[!] Debe terminar en .pkl\n"); continue
            try:
                out.parent.mkdir(parents=True, exist_ok=True)
                self.guardar_pkl(out)
                print(f"[OK] Guardado en {out.resolve()}")
                break
            except Exception as e:
                print(f"[!] {e}\n")

if __name__ == "__main__":
    Directorio().menu()
