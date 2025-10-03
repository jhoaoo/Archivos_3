with open("archivobase.txt", "w", encoding="utf-8") as f:
    f.write("Lenguaje de Programación I\n")
    f.write("Python es un lenguaje poderoso\n")
    f.write("Manejo de archivos con with\n")

print("Archivo 'archivobase.txt' creado con éxito ")

#Actividad4.py
import re
def leer_archivo(nombre):
    try:
        with open(nombre, "r", encoding="utf-8") as archi:
            print(" Contenido del archivo:")
            for linea in archi:
                linea_limpia = re.sub(r"\n", "", linea)
                print(linea_limpia)
    except FileNotFoundError:
        print(f" El archivo '{nombre}' no existe.")
    except Exception as e:
        print(" Error inesperado:", e)
nombre = input("Digite nombre del archivo completo: ")
leer_archivo(nombre)
