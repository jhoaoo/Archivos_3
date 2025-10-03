import pickle
import os

class Pelicula:
    def __init__(self,titulo,duracion,anio):
        self.titulo=titulo
        self.duracion=duracion
        self.anio=anio
    def mostrar(self):
        return f"Titulo:{self.titulo},Duracion:{self.duracion},Año:{self.anio}"

if __name__=="__main__":
    archivo="peliculas.pickl"
    if os.path.exists(archivo):
        try:
            with open(archivo,"rb") as f:
                peliculas=pickle.load(f)
                if peliculas:
                    for p in peliculas:
                        print(p.mostrar())
                else:
                    print("No hay peliculas almacenadas")
        except Exception:
            print("Error al leer el archivo")
    else:
        print("El archivo no existe")
