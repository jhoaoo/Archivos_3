from __future__ import annotations
import re, pandas as pd
from dataclasses import dataclass, asdict
from pathlib import Path

class ErrorProducto(Exception): ...

RX_NOM = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ 0-9\-]{2,60}$")
RX_PREC = re.compile(r"^\d+(\.\d{1,2})?$")
RX_STK = re.compile(r"^\d+$")

@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int

    @staticmethod
    def crear(nombre: str, precio_s: str, stock_s: str) -> "Producto":
        if not RX_NOM.fullmatch(nombre.strip()): raise ErrorProducto("Nombre inválido")
        if not RX_PREC.fullmatch(precio_s): raise ErrorProducto("Precio inválido (hasta 2 decimales)")
        if not RX_STK.fullmatch(stock_s): raise ErrorProducto("Stock inválido (entero >=0)")
        precio = float(precio_s); stock = int(stock_s)
        if precio <= 0: raise ErrorProducto("Precio debe ser > 0")
        return Producto(nombre.strip(), precio, stock)

class Tienda:
    def __init__(self, archivo: Path):
        self.archivo = archivo
        self.items: dict[str, Producto] = {}
        self.cargar()

    def cargar(self) -> None:
        self.items.clear()
        if not self.archivo.exists(): return
        for linea in self.archivo.read_text(encoding="utf-8").splitlines():
            if not linea.strip(): continue
            # formato: nombre|precio|stock
            partes = linea.split("|")
            if len(partes)!=3: continue
            try:
                p = Producto.crear(partes[0], partes[1], partes[2])
                self.items[p.nombre] = p
            except ErrorProducto:
                continue

    def guardar(self) -> None:
        lineas = [f"{p.nombre}|{p.precio}|{p.stock}" for p in self.items.values()]
        self.archivo.write_text("\n".join(lineas), encoding="utf-8")

    def agregar(self, p: Producto) -> None:
        self.items[p.nombre] = p; self.guardar()

    def listar_df(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(p) for p in self.items.values()]) if self.items else pd.DataFrame(columns=["nombre","precio","stock"])

    def buscar(self, nombre: str) -> Producto | None:
        return self.items.get(nombre)

    def actualizar_precio(self, nombre: str, nuevo_precio_s: str) -> None:
        if nombre not in self.items: raise ErrorProducto("Producto no existe")
        if not RX_PREC.fullmatch(nuevo_precio_s): raise ErrorProducto("Precio inválido")
        nuevo = float(nuevo_precio_s)
        if nuevo <= 0: raise ErrorProducto("Precio debe ser > 0")
        self.items[nombre].precio = nuevo; self.guardar()

    def eliminar(self, nombre: str) -> None:
        if nombre in self.items:
            del self.items[nombre]; self.guardar()

def pedir_archivo() -> Path:
    while True:
        ruta = Path(input("Archivo de productos [productos.txt]: ").strip() or "productos.txt")
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            if not ruta.exists(): ruta.write_text("", encoding="utf-8")
            return ruta
        except Exception as e:
            print(f"[!] {e}\n")

def menu():
    print("=== Gestión de Productos ===")
    ruta = pedir_archivo()
    tienda = Tienda(ruta)
    while True:
        print("\n1) Agregar  2) Listar  3) Buscar  4) Actualizar precio  5) Eliminar  6) Salir")
        op = input("Opción: ").strip()
        if op not in {"1","2","3","4","5","6"}:
            print("[!] Opción inválida"); continue
        if op=="1":
            n = input("Nombre: ").strip()
            p = input("Precio: ").strip()
            s = input("Stock: ").strip()
            try:
                tienda.agregar(Producto.crear(n,p,s)); print("[OK] Agregado.")
            except ErrorProducto as e: print(f"[!] {e}")
        elif op=="2":
            df = tienda.listar_df(); print(df.to_string(index=False))
        elif op=="3":
            n = input("Nombre a buscar: ").strip()
            prod = tienda.buscar(n); print(prod if prod else "No encontrado")
        elif op=="4":
            n = input("Nombre: ").strip()
            np = input("Nuevo precio: ").strip()
            try:
                tienda.actualizar_precio(n, np); print("[OK] Actualizado.")
            except ErrorProducto as e: print(f"[!] {e}")
        elif op=="5":
            n = input("Nombre a eliminar: ").strip()
            tienda.eliminar(n); print("[OK] Eliminado (si existía).")
        else:
            break

if __name__ == "__main__":
    menu()
