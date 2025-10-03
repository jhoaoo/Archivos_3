
import re, pandas as pd
from pathlib import Path

def pedir_txt(mensaje="Ruta .txt: ") -> Path:
    while True:
        ruta = Path(input(mensaje).strip())
        try:
            if ruta.suffix.lower()!=".txt": raise ValueError("Debe ser .txt")
            ruta.read_text(encoding="utf-8")
            return ruta
        except Exception as e:
            print(f"[!] {e}\n")

def main():
    print("=== Buscar/Reemplazar en TXT ===")
    ruta = pedir_txt()
    patron = input("Patrón (regex) a buscar: ").strip()
    reemplazo = input("Texto de reemplazo: ").strip()
    try:
        rx = re.compile(patron, flags=re.UNICODE)
    except re.error as e:
        print(f"[!] Regex inválida: {e}")
        return
    texto = ruta.read_text(encoding="utf-8")
    nuevo, n = rx.subn(reemplazo, texto)
    df = pd.DataFrame([{"archivo": str(ruta), "reemplazos_realizados": n}])
    print(df.to_string(index=False))
    out = pedir_txt("Guardar como .txt (nuevo): ")
    out.write_text(nuevo, encoding="utf-8")
    print(f"[OK] Guardado en {out.resolve()}")

if __name__ == "__main__":
    main()
