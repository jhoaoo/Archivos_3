#Actividad 7.py
import pickle
import re
def validar_lista(lista):
    if not lista:
        raise ValueError("La lista está vacía.")
    for item in lista:
        if not isinstance(item, int) or not re.fullmatch(r'[1-9]\d{0,2}', str(item)):
            raise ValueError(f"Elemento inválido en la lista: {item}")
def guardar_pickle(lista, nombre_archivo):
    try:
        validar_lista(lista)
        with open(nombre_archivo, 'wb') as archivo:
            pickle.dump(lista, archivo)
        print(f"Archivo '{nombre_archivo}' creado correctamente con la lista: {lista}")
    except ValueError as ve:
        print(f"Error de validación: {ve}")
    except Exception as e:
        print(f"Error al guardar el archivo pickle: {e}")
def main():
    lista = [1, 2, 3, 4, 5] 
    guardar_pickle(lista, 'actividad7.pckl')
if __name__ == "__main__":
    main()
