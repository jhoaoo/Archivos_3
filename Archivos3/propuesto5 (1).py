
import re, pandas as pd
from pathlib import Path

def pedir_txt() -> Path:
    while True:
        ruta = Path(input("Ruta .txt: ").strip())
        try:
            if ruta.suffix.lower() != ".txt": raise ValueError("Debe ser .txt")
            ruta.read_text(encoding="utf-8")
            return ruta
        except Exception as e:
            print(f"[!] {e}\n")

def frec_letras(ruta: Path) -> dict[str,int]:
    txt = ruta.read_text(encoding="utf-8", errors="replace").lower()
    letras = re.findall(r"[a-záéíóúüñ]", txt, flags=re.UNICODE)
    freq = {}
    for ch in letras:
        freq[ch] = freq.get(ch,0)+1
    return dict(sorted(freq.items()))

def main():
    print("=== Frecuencia de Letras ===")
    ruta = pedir_txt()
    freq = frec_letras(ruta)
    if not freq:
        print("(sin letras)"); return
    df = pd.DataFrame(list(freq.items()), columns=["letra","frecuencia"])
    print(df.to_string(index=False))
    out = Path(input("Guardar reporte .txt [reporte_letras.txt]: ").strip() or "reporte_letras.txt")
    out.write_text(df.to_string(index=False), encoding="utf-8")
    print(f"[OK] Guardado en {out.resolve()}")

if __name__ == "__main__":
    main()
