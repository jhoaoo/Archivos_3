def crear_archivo_binario(ruta, tamano=10, inicio=10):
    datos = bytearray(tamano)
    for i in range(tamano):
        datos[i] = inicio + i  
    try:
        with open(ruta, 'wb') as fichero:
            fichero.write(datos)
        print(f"Archivo '{ruta}' creado con {tamano} bytes válidos.")
    except Exception as e:
        print(f"Error al crear el archivo: {e}")
if __name__ == "__main__":
    crear_archivo_binario('actividad6.bin')

#Actividad 6.py
import re
def validar_byte(valor):
    hex_val = format(valor, '02x') 

    return bool(re.fullmatch(r'0[a-f]|1[0-9a-d]', hex_val))
def leer_archivo_binario(ruta, tamano=10):
    datos = bytearray(tamano)
    try:
        with open(ruta, 'rb') as fichero:
            num_bytes = fichero.readinto(datos) 
        print(f"Se leyeron {num_bytes} bytes del archivo '{ruta}':")
        for b in datos:
            if validar_byte(b):
                print(hex(b), end=' ')
            else:
                print(f"\nValor inválido encontrado en byte: {b} ({hex(b)})")
                break
        else:
            print("\nTodos los bytes son válidos.")
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta}' no fue encontrado.")
    except Exception as e:
        print(f"Error al abrir o leer el fichero: {e}")
def main():
    leer_archivo_binario('actividad6.bin', 10)
if __name__ == "__main__":
    main()

