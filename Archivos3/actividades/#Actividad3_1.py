with open("archivo.txt", "w", encoding="utf-8") as f:
    f.write("3\n")
    f.write("4\n")
    f.write("5\n")
    f.write("6\n")
    f.write("hola\n")   
    f.write("10\n")
print("Archivo 'archivo.txt' creado con éxito.")

#Actividad3_1.py
from io import open
import re
def leer_numeros(nombre):
    try:
        archi = open(nombre, "r", encoding="utf-8")
        suma = 0
        contador = 0
        ln = archi.readline()
        while ln:
            try:
                if re.fullmatch(r'-?\d+', ln.strip()):
                    suma += int(ln.strip())
                    contador += 1
                else:
                    print(f" Línea inválida: {ln.strip()} (no es un número)")
            except Exception as e:
                print(f" Error procesando línea: {e}")
            ln = archi.readline()
        if contador > 0:
            print(" Resultados:")
            print("Suma =", suma)
            print("Promedio =", suma / contador)
        else:
            print(" No se encontraron números válidos en el archivo.")
        archi.close()
    except FileNotFoundError:
        print(f" No existe el archivo llamado '{nombre}'.")
    except Exception as e:
        print(f" Error inesperado: {e}")
nombre = input("Digite nombre del archivo completo: ")
leer_numeros(nombre)
