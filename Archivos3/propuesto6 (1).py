
import re, pandas as pd
from pathlib import Path

RX_TXT = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$")

def contar_vocales(s: str) -> dict[str,int]:
    mapa = {"a":"aáä", "e":"eéë", "i":"iíï", "o":"oóö", "u":"uúü"}
    out = {k:0 for k in "aeiou"}
    total = 0
    for ch in s.lower():
        for base, grupo in mapa.items():
            if ch in grupo:
                out[base]+=1; total+=1; break
    out["total"]=total
    return out

def main():
    print("=== Conteo de Vocales ===")
    while True:
        s = input("Ingrese una oración (solo letras y espacios): ").strip()
        if RX_TXT.fullmatch(s): break
        print("[!] Entrada inválida. Intente nuevamente.\n")
    conteo = contar_vocales(s)
    df = pd.DataFrame([conteo])
    print(df.to_string(index=False))
    out = Path(input("Guardar resultado .txt [vocales.txt]: ").strip() or "vocales.txt")
    out.write_text(df.to_string(index=False), encoding="utf-8")
    print(f"[OK] Guardado en {out.resolve()}")

if __name__ == "__main__":
    main()
