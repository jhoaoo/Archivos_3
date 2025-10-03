#Actividad 8.py
import pickle
import re
def validar_lista(lista):
    if not isinstance(lista, list) or not lista:
        raise ValueError("El contenido no es una lista válida o está vacía.")
    for item in lista:
        if not isinstance(item, int) or not re.fullmatch(r'[1-9]\d{0,2}', str(item)):
            raise ValueError(f"Elemento inválido en la lista: {item}")
def leer_pickle(nombre_archivo):
    try:
        with open(nombre_archivo, 'rb') as archivo:
            lista = pickle.load(archivo)

        validar_lista(lista)
        print(f"Contenido válido leído del archivo '{nombre_archivo}': {lista}")
        return lista
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
    except (pickle.UnpicklingError, EOFError):
        print(f"Error: El archivo '{nombre_archivo}' está corrupto o no es un archivo pickle válido.")
    except ValueError as ve:
        print(f"Error de validación: {ve}")
    except Exception as e:
        print(f"Error inesperado al leer el archivo pickle: {e}")
def main():
    leer_pickle('actividad7.pckl')
if __name__ == "__main__":
    main()
