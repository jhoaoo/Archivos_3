def es_png(archivo):
    firma=b'\x89PNG\r\n\x1a\n'
    with open(archivo,"rb") as f:
        cabecera=f.read(8)
    return cabecera==firma

if __name__=="__main__":
    nombre=input("Ingrese el nombre del archivo: ")
    try:
        if es_png(nombre):
            print("El archivo es PNG")
        else:
            print("El archivo no es PNG")
    except FileNotFoundError:
        print("El archivo no existe")
    except Exception as e:
        print(f"Error:{e}")
