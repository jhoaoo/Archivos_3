#Actividad1_3.py
from io import open
import re
try:
    archi = open("archivo.txt", "r")
    lineas = archi.readlines()
    if lineas:
        primera_linea = lineas[0].strip()
        if re.fullmatch(r'[\w\sÁÉÍÓÚáéíóúÑñ.!¡]+', primera_linea):
            print(" Primera línea del archivo:")
            print(primera_linea)
        else:
            print(" La primera línea contiene caracteres no válidos.")
    else:
        print(" El archivo está vacío.")
    archi.close()
except FileNotFoundError:
    print(" No existe el archivo. Ejecute primero el ejercicio 1.")
except Exception as e:
    print(f" Error al leer línea por línea: {e}")
