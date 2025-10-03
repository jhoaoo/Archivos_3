#Actividad1_2.py
from io import open
import re
try:
    archi = open("archivo.txt", "r")
    contenido = archi.read()
    if re.fullmatch(r'[\w\sÁÉÍÓÚáéíóúÑñ.!¡]*', contenido):
        if contenido.strip():
            print(" Contenido del archivo:")
            print(contenido)
        else:
            print(" El archivo está vacío.")
    else:
        print(" El contenido tiene caracteres no permitidos.")
    archi.close()
except FileNotFoundError:
    print(" No existe el archivo. Ejecute primero el ejercicio 1.")
except Exception as e:
    print(f" Error al leer el archivo: {e}")

