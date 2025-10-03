#Actividad1_1.py
from io import open
import re
try:
    archi = open("archivo.txt", "w") 
    texto = "La vida es bella!!!"
    if re.match(r'^[\w\s¡!]+$', texto):
        archi.write(texto)
        print(" Texto escrito correctamente en el archivo.")
    else:
        print(" El texto contiene caracteres no permitidos.")
    archi.close()
except Exception as e:
    print(f" Ocurrió un error: {e}")
