
import re, pandas as pd
from pathlib import Path

def pedir_txt() -> Path:
    while True:
        ruta = Path(input("Ruta .txt: ").strip().strip('"').strip("'"))
        try:
            if ruta.suffix.lower() != ".txt": raise ValueError("Debe ser .txt")
            ruta.read_text(encoding="utf-8")
            return ruta
        except Exception as e:
            print(f"[!] {e}. Intente nuevamente.\n")

def tokens(ruta: Path) -> list[str]:
    txt = ruta.read_text(encoding="utf-8", errors="replace").lower()
    return re.findall(r"\b\w+\b", txt, flags=re.UNICODE)

def main():
    print("=== Conteo de Palabras ===")
    ruta = pedir_txt()
    objetivo = input("Palabra a buscar (opcional): ").strip().lower()
    toks = tokens(ruta)
    total = len(toks)
    coincidencias = sum(1 for t in toks if objetivo and t == objetivo)
    df = pd.DataFrame([{"archivo": str(ruta), "total_palabras": total, "coincidencias": coincidencias}])
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
