#Actividad1_4.py
from io import open
import re
try:
    archi = open("archivo.txt", "a")  
    nueva_linea = "\nLa actitud siempre debe ser positiva"
    if re.fullmatch(r'[\w\sÁÉÍÓÚáéíóúÑñ.!¡]+', nueva_linea.strip()):
        archi.write(nueva_linea)
        print(" Línea agregada correctamente.")
    else:
        print(" La línea no cumple con el formato permitido.")
    archi.close()
except Exception as e:
    print(f" Error al agregar línea: {e}")
