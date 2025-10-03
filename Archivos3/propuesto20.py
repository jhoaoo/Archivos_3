import pickle
import os

class Pelicula:
    def __init__(self,titulo,duracion,anio):
        self.titulo=titulo
        self.duracion=duracion
        self.anio=anio
    def mostrar(self):
        return f"Titulo:{self.titulo},Duracion:{self.duracion},Año:{self.anio}"

class Catalogo:
    def __init__(self,archivo="peliculas.pickl"):
        self.archivo=archivo
        self.peliculas=self.cargar()
    def agregar(self,pelicula):
        self.peliculas.append(pelicula)
        self.guardar()
    def mostrar(self):
        if not self.peliculas:
            print("No hay peliculas")
        else:
            for p in self.peliculas:
                print(p.mostrar())
    def guardar(self):
        with open(self.archivo,"wb") as f:
            pickle.dump(self.peliculas,f)
    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo,"rb") as f:
                    return pickle.load(f)
            except Exception:
                return []
        return []

if __name__=="__main__":
    catalogo=Catalogo()
    p1=Pelicula("Matrix",120,1999)
    p2=Pelicula("Inception",148,2010)
    p3=Pelicula("Interstellar",169,2014)
    catalogo.agregar(p1)
    catalogo.agregar(p2)
    catalogo.agregar(p3)
    catalogo.mostrar()
