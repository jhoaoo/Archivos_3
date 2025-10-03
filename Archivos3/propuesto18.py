import pickle
import os

class Tarea:
    def __init__(self,descripcion,fecha_vencimiento,estado="pendiente"):
        self.descripcion=descripcion
        self.fecha_vencimiento=fecha_vencimiento
        self.estado=estado
    def completar(self):
        self.estado="finalizada"
    def mostrar(self):
        return f"Descripcion:{self.descripcion},Vencimiento:{self.fecha_vencimiento},Estado:{self.estado}"

class GestorTareas:
    def __init__(self,archivo="tareas.pickl"):
        self.archivo=archivo
        self.tareas=self.cargar()
    def agregar(self,tarea):
        self.tareas.append(tarea)
        self.guardar()
    def listar(self):
        if not self.tareas:
            print("No hay tareas")
        else:
            for t in self.tareas:
                print(t.mostrar())
    def guardar(self):
        with open(self.archivo,"wb") as f:
            pickle.dump(self.tareas,f)
    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo,"rb") as f:
                    return pickle.load(f)
            except Exception:
                return []
        return []

if __name__=="__main__":
    gestor=GestorTareas()
    t1=Tarea("Estudiar para el examen","2025-10-05")
    t2=Tarea("Entregar informe","2025-10-07")
    t3=Tarea("Preparar presentacion","2025-10-10")
    gestor.agregar(t1)
    gestor.agregar(t2)
    gestor.agregar(t3)
    gestor.listar()
    t1.completar()
    gestor.guardar()
    print("Despues de completar una tarea:")
    gestor.listar()
