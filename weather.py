import requests
import gzip
import json
from io import BytesIO

class Respuesta:
    def __init__(self, data):
        self.cc = data.get('cc')
        self.desciel = data.get('desciel')
        self.dh = data.get('dh')
        self.dirvienc = data.get('dirvienc')
        self.dirvieng = data.get('dirvieng')
        self.dloc = data.get('dloc')
        self.ides = data.get('ides')
        self.idmun = data.get('idmun')
        self.lat = data.get('lat')
        self.lon = data.get('lon')
        self.ndia = data.get('ndia')
        self.nes = data.get('nes')
        self.nmun = data.get('nmun')
        self.prec = data.get('prec')
        self.probprec = data.get('probprec')
        self.raf = data.get('raf')
        self.tmax = data.get('tmax')
        self.tmin = data.get('tmin')
        self.velvien = data.get('velvien')
    
    def __repr__(self):
        return (
            f"Respuesta(\n"
            f"  cc={self.cc},\n"
            f"  desciel='{self.desciel}',\n"
            f"  dh={self.dh},\n"
            f"  dirvienc='{self.dirvienc}',\n"
            f"  dirvieng='{self.dirvieng}',\n"
            f"  dloc='{self.dloc}',\n"
            f"  ides={self.ides},\n"
            f"  idmun={self.idmun},\n"
            f"  lat={self.lat},\n"
            f"  lon={self.lon},\n"
            f"  ndia={self.ndia},\n"
            f"  nes='{self.nes}',\n"
            f"  nmun='{self.nmun}',\n"
            f"  prec={self.prec},\n"
            f"  probprec={self.probprec},\n"
            f"  raf={self.raf},\n"
            f"  tmax={self.tmax},\n"
            f"  tmin={self.tmin},\n"
            f"  velvien={self.velvien}\n"
            f")"
        )

class WeatherDataProcessor:
    def __init__(self, url):
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
    
    def buscar_estado(self, estado_buscado):
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
                print(f"- {municipio}")
        else:
            print(f"No se encontraron municipios para el estado '{estado_buscado}'.")

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
                print(f"- {estado}")
        else:
            print("No se encontraron estados en los datos.")
    
    def mostrar_datos_estado_municipio(self, estado_buscado, municipio_buscado):
        """Muestra todos los datos para un estado y municipio específicos."""
        if self.data is None:
            print("No se han obtenido datos.")
            return
        
        encontrados = False
        for item in self.data:
            if item.get('nes') == estado_buscado and item.get('nmun') == municipio_buscado:
                print(f"Datos para el estado '{estado_buscado}' y municipio '{municipio_buscado}':")
                print(f"  cc: {item.get('cc')}")
                print(f"  desciel: {item.get('desciel')}")
                print(f"  dh: {item.get('dh')}")
                print(f"  dirvienc: {item.get('dirvienc')}")
                print(f"  dirvieng: {item.get('dirvieng')}")
                print(f"  dloc: {item.get('dloc')}")
                print(f"  ides: {item.get('ides')}")
                print(f"  idmun: {item.get('idmun')}")
                print(f"  lat: {item.get('lat')}")
                print(f"  lon: {item.get('lon')}")
                print(f"  ndia: {item.get('ndia')}")
                print(f"  nes: {item.get('nes')}")
                print(f"  nmun: {item.get('nmun')}")
                print(f"  prec: {item.get('prec')}")
                print(f"  probprec: {item.get('probprec')}")
                print(f"  raf: {item.get('raf')}")
                print(f"  tmax: {item.get('tmax')}")
                print(f"  tmin: {item.get('tmin')}")
                print(f"  velvien: {item.get('velvien')}")
                encontrados = True
        
        if not encontrados:
            print(f"No se encontraron datos para el estado '{estado_buscado}' y municipio '{municipio_buscado}'.")

def main():
    url = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"
    estado_buscado = "Estado de México"  # Nombre del estado que deseas buscar
    municipio_buscado = "Nezahualcóyotl"  # Nombre del municipio que deseas buscar

    processor = WeatherDataProcessor(url)
    processor.obtener_datos()
    
    # Listar todos los estados
    #processor.listar_estados()
    
    # Buscar municipios en el estado específico
    #processor.buscar_estado(estado_buscado)
    
    # Mostrar datos para un estado y municipio específicos
    processor.mostrar_datos_estado_municipio(estado_buscado, municipio_buscado)

if __name__ == "__main__":
    main()