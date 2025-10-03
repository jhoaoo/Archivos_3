#Actividad10_1.py
import pickle
import re
class Vehiculo:
    def __init__(self, firma, version):
        if not re.fullmatch(r"[A-Za-z0-9 ]+", firma):
            raise ValueError("La marca contiene caracteres no válidos")
        if not re.fullmatch(r"[A-Za-z0-9 ]+", version):
            raise ValueError("El modelo contiene caracteres no válidos")
        self.firma = firma
        self.version = version
        self.en_marcha = False
        self.acelerando = False
        self.frenando = False
    def arrancar(self):
        self.en_marcha = True
    def acelerar(self):
        self.acelerando = True
    def frenar(self):
        self.frenando = True
    def estado(self):
        return f"Marca: {self.firma}\nModelo: {self.version}\nEn marcha: {self.en_marcha}\nAcelerando: {self.acelerando}\nFrenando: {self.frenando}\n-------------------------"
try:
    auto1 = Vehiculo("Honda", "CRV")
    auto2 = Vehiculo("Toyota", "Yaris")
    auto3 = Vehiculo("Nissan", "Sentra")
    autos = [auto1, auto2, auto3]
    with open("actividad5.pckl", "wb") as archivo_binario:
        pickle.dump(autos, archivo_binario)
    with open("actividad5.pckl", "rb") as archivo_apertura:
        vehiculos = pickle.load(archivo_apertura)
    print(" Vehículos cargados desde archivo:")
    for item in vehiculos:
        print(item.estado())
except Exception as e:
    print(" Error en la serialización:", e)
