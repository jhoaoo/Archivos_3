#Actividad2_2.py
from io import open
import re
def crearArchivo(texto):
    try:
        archi = open("prueba.txt", "w", encoding="utf-8")
        if re.fullmatch(r'[\w\sÁÉÍÓÚáéíóúÑñ.,;:!?¡¿-]+', texto):
            archi.write("Lenguaje de Programación I\n")
            archi.write(texto)
            print(" Archivo creado y texto escrito correctamente.")
        else:
            print(" El texto contiene caracteres no permitidos.")
        archi.close()
    except Exception as e:
        print(f" Error al crear archivo: {e}")
texto = input("Ingrese un texto a agregar al archivo: ")
crearArchivo(texto)
