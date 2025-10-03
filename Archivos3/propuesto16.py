def es_jpg(archivo):
    firma=b'\xFF\xD8'
    with open(archivo,"rb") as f:
        cabecera=f.read(2)
    return cabecera==firma

if __name__=="__main__":
    nombre=input("Ingrese el nombre del archivo: ")
    try:
        if es_jpg(nombre):
            print("El archivo es JPG")
        else:
            print("El archivo no es JPG")
    except FileNotFoundError:
        print("El archivo no existe")
    except Exception as e:
        print(f"Error:{e}")

