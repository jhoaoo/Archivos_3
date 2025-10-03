#Actividad 5.py
import re
def validar_valor(valor):
    return bool(re.fullmatch(r'1[0-9]', str(valor)))
def crear_bytearray(tamano, inicio=10):
    datos = bytearray(tamano)
    for i in range(tamano):
        valor = inicio + i
        if validar_valor(valor):
            datos[i] = valor
        else:
            raise ValueError(f"Valor inválido para bytearray: {valor}")
    return datos
def guardar_binario(datos, ruta):
    try:
        with open(ruta, 'wb') as fichero:
            fichero.write(datos)
        print(f"Archivo '{ruta}' guardado correctamente.")
    except Exception as e:
        print(f"Error al abrir o escribir el fichero: {e}")
def main():
    try:
        datos = crear_bytearray(10, 10)
        print("Datos a escribir en el archivo binario:", list(datos))
        guardar_binario(datos, 'actividad5.bin')
    except ValueError as ve:
        print(f"Validación fallida: {ve}")
    except Exception as e:
        print(f"Error inesperado: {e}")
if __name__ == "__main__":
    main()
