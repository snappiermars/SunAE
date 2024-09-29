import requests
import gzip
import json
from io import BytesIO

class WeatherDataProcessor:
    def __init__(self, url="https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"):
        self.url = url
        self.data = None
    
    def obtener_datos(self):
        """Obtiene y descomprime los datos de la URL proporcionada."""
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()  # Lanza un error si la solicitud no es exitosa

            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                self.data = json.load(gz)
                if not isinstance(self.data, list):
                    raise ValueError("La respuesta de la API no es una lista.")
        except requests.RequestException as e:
            print(f"Excepción Capturada: {e}")
            self.data = None
        except ValueError as e:
            print(f"Excepción Capturada: {e}")
            self.data = None
    
    def listar_municipios(self, estado_buscado):
        """Busca y muestra los municipios para un estado específico."""
        if self.data is None:
            print("No se han obtenido datos.")
            return
        
        municipios = set()
        for item in self.data:
            if item.get('nes') == estado_buscado:
                municipio = item.get('nmun')
                if municipio:
                    municipios.add(municipio)
        
        if municipios:
            print(f"Municipios en el estado '{estado_buscado}':")
            for municipio in municipios:
                print(f"{municipio}")
        else:
            print(f"No se encontraron municipios para el estado '{estado_buscado}'.")
        return sorted(municipios)

    def listar_estados(self):
        """Lista todos los estados disponibles en los datos."""
        if self.data is None:
            print("No se han obtenido datos.")
            return
        
        estados = set()
        for item in self.data:
            estado = item.get('nes')
            if estado:
                estados.add(estado)
        
        if estados:
            print("Estados disponibles:")
            for estado in sorted(estados):
                print(f"{estado}")
        else:
            print("No se encontraron estados en los datos.")
        return sorted(estados)
    
    def mostrar_datos_estado_municipio(self, estado_buscado, municipio_buscado):
        """Muestra todos los datos para un estado y municipio específicos."""
        if self.data is None:
            print("No se han obtenido datos.")
            return None
    
        datos_municipio = []  # Lista para almacenar todos los datos encontrados
        for item in self.data:
            if item.get('nes') == estado_buscado and item.get('nmun') == municipio_buscado:
                datos = {
                    "cc": item.get('cc'),
                    "desciel": item.get('desciel'),
                    "dh": item.get('dh'),
                    "dirvienc": item.get('dirvienc'),
                    "dirvieng": item.get('dirvieng'),
                    "dloc": item.get('dloc'),
                    "ides": item.get('ides'),
                    "idmun": item.get('idmun'),
                    "lat": item.get('lat'),
                    "lon": item.get('lon'),
                    "ndia": item.get('ndia'),
                    "nes": item.get('nes'),
                    "nmun": item.get('nmun'),
                    "prec": item.get('prec'),
                    "probprec": item.get('probprec'),
                    "raf": item.get('raf'),
                    "tmax": item.get('tmax'),
                    "tmin": item.get('tmin'),
                    "velvien": item.get('velvien'),
                }
                datos_municipio.append(datos)  # Agregar el diccionario a la lista
    
        if not datos_municipio:
            print(f"No se encontraron datos para el estado '{estado_buscado}' y municipio '{municipio_buscado}'.")
            return None

        return datos_municipio  # Retornar la lista con los datos


def main():
    url = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"
    estado_buscado = "Estado de México"  # Nombre del estado que deseas buscar
    municipio_buscado = "Nezahualcóyotl"  # Nombre del municipio que deseas buscar

    processor = WeatherDataProcessor(url)
    processor.obtener_datos()
    
    #Listar todos los estados
    #processor.listar_estados()
    
    # Buscar municipios en el estado específico
    #processor.listar_municipios(estado_buscado)
    
    datos = processor.mostrar_datos_estado_municipio(estado_buscado, municipio_buscado)
    if datos:
        for registro in datos:
            print(registro)  # Imprimir cada registro encontrado

if __name__ == "__main__":
    main()