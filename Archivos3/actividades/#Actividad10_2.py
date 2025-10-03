#Actividad10_2.py
import pickle
import re
class Docente:
    def __init__(self, nombre, edad, horas):
        if not re.fullmatch(r"[A-Za-z ]+", nombre):
            raise ValueError("El nombre solo puede contener letras y espacios")
        if not isinstance(edad, int) or not isinstance(horas, int):
            raise ValueError("Edad y horas deben ser números enteros")
        self.nombre = nombre
        self.edad = edad
        self.horas = horas
        print(" Creación de nuevo docente:", self.nombre)
    def __str__(self):
        return f"{self.nombre} - Edad: {self.edad}, Horas: {self.horas}"
class ListaDocentes:
    def __init__(self):
        try:
            with open("actividad6.bin", "rb") as listaDeDocentes:
                self.docentes = pickle.load(listaDeDocentes)
                print(f" Se cargaron {len(self.docentes)} docentes desde el archivo.")
        except (EOFError, FileNotFoundError):
            self.docentes = []
            print(" El archivo está vacío o no existe, se creará uno nuevo.")
    def agregarDocente(self, d):
        self.docentes.append(d)
        self.guardarDocentesEnArchivo()
    def mostrarDocentes(self):
        for d in self.docentes:
            print(d)
    def guardarDocentesEnArchivo(self):
        with open("actividad6.bin", "wb") as listaDeDocentes:
            pickle.dump(self.docentes, listaDeDocentes)
    def mostrarInformacionArchivo(self):
        print(" Información del archivo actual:")
        for docente in self.docentes:
            print(docente)
try:
    miLista = ListaDocentes()
    miLista.agregarDocente(Docente("Dely", 43, 30))
    miLista.agregarDocente(Docente("Miguel", 24, 24))
    miLista.agregarDocente(Docente("Leandro", 30, 18))
    print("\n Lista de docentes en memoria:")
    miLista.mostrarDocentes()
    print("\n Lectura desde el archivo .bin:")
    miLista.mostrarInformacionArchivo()
except Exception as e:
    print(" Error en la gestión de docentes:", e)
