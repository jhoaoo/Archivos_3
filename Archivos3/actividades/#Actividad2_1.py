#Actividad2_1.py
from io import open
import re
try:
    archi = open("archivo.txt", "w")
    nombre = archi.name
    cerrado = archi.closed
    modo = archi.mode
    if re.fullmatch(r'.+\.txt', nombre) and re.fullmatch(r'[rwa]{1}', modo):
        print(" Información del archivo:")
        print("Nombre:", nombre)
        print("Está cerrado:", cerrado)
        print("Modalidad de apertura:", modo)
    else:
        print(" El archivo no cumple con la validación esperada.")
    archi.close()
except Exception as e:
    print(f" Error al mostrar información del archivo: {e}")
