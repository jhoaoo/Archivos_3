#Actividad 9.py
import re
class TipoImagen:
    @staticmethod
    def chequearImagenBMP(archivo):
        try:
            if not re.fullmatch(r'.+\.bmp', archivo, re.IGNORECASE):
                print(f"Advertencia: El archivo '{archivo}' no tiene extensión '.bmp'.")
            with open(archivo, "rb") as archivo_binario:
                contenido = archivo_binario.read(2)
                if len(contenido) < 2:
                    print(f"Error: El archivo '{archivo}' es demasiado pequeño para ser un BMP válido.")
                    return False
                if contenido[0] == 0x42 and contenido[1] == 0x4D:
                    return True
                else:
                    return False
        except FileNotFoundError:
            print(f"Error: El archivo '{archivo}' no existe.")
            return False
        except PermissionError:
            print(f"Error: No tienes permiso para abrir el archivo '{archivo}'.")
            return False
        except Exception as e:
            print(f"Error inesperado al procesar el archivo '{archivo}': {e}")
            return False
def main():
    archivos_prueba = [
        "imagen_bmp.bmp",
        "imagen_jpg.jpg",
        "imagen_png.png",
        "archivo_inexistente.bmp",
        "archivo_pequeño.bmp"
    ]
    for archivo in archivos_prueba:
        resultado = TipoImagen.chequearImagenBMP(archivo)
        print(f"¿El archivo '{archivo}' es BMP? -> {resultado}")
if __name__ == "__main__":
    main()
