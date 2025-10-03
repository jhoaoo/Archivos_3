import pickle
import re
import os

class Personaje:
    def __init__(self,nombre,vida,ofensiva,proteccion,alcance):
        if not re.fullmatch(r"[A-Za-z0-9]+",nombre):
            raise ValueError("El nombre solo puede contener letras o numeros")
        for atributo,valor in {"vida":vida,"ofensiva":ofensiva,"proteccion":proteccion,"alcance":alcance}.items():
            if not re.fullmatch(r"\d+",str(valor)) or int(valor)<=0:
                raise ValueError(f"{atributo} debe ser un numero entero positivo")
        self.nombre=nombre
        self.vida=int(vida)
        self.ofensiva=int(ofensiva)
        self.proteccion=int(proteccion)
        self.alcance=int(alcance)
    def __str__(self):
        return f"{self.nombre}->Vida:{self.vida},Ofensiva:{self.ofensiva},Proteccion:{self.proteccion},Alcance:{self.alcance}"

class Gestor:
    def __init__(self,archivo="personajes.pickl"):
        self.archivo=archivo
        self.personajes=self.cargar()
    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo,"rb") as f:
                    return pickle.load(f)
            except Exception:
                return {}
        return {}
    def guardar(self):
        with open(self.archivo,"wb") as f:
            pickle.dump(self.personajes,f)
    def agregar(self,personaje):
        if personaje.nombre in self.personajes:
            print(f"El personaje '{personaje.nombre}' ya existe")
        else:
            self.personajes[personaje.nombre]=personaje
            self.guardar()
            print(f"Personaje '{personaje.nombre}' agregado")
    def mostrar(self):
        if not self.personajes:
            print("No hay personajes")
        else:
            for p in self.personajes.values():
                print(p)
    def borrar(self,nombre):
        if nombre in self.personajes:
            del self.personajes[nombre]
            self.guardar()
            print(f"Personaje '{nombre}' eliminado")
        else:
            print(f"No se encontro el personaje '{nombre}'")

if __name__=="__main__":
    gestor=Gestor()
    try:
        p1=Personaje("Personaje1",4,2,4,2)
        p2=Personaje("Personaje2",2,4,2,4)
        p3=Personaje("Personaje3",2,4,1,8)
        gestor.agregar(p1)
        gestor.agregar(p2)
        gestor.agregar(p3)
        gestor.mostrar()
        gestor.borrar("Personaje3")
        gestor.mostrar()
    except Exception as e:
        print(f"Error:{e}")
