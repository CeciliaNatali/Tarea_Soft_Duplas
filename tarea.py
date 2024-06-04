import csv
import requests
from math import radians, cos, sin, asin, sqrt

class Coordenada:
    def _init_(self, latitud, longitud) -> None:
        self.latitud = latitud
        self.longitud = longitud

class Ciudad:
    def _init_(self, pais, ciudad) -> None:
        self.pais = pais
        self.ciudad = ciudad 


class GetCoordenada:
    def get_coordenada(self, ciudad):
        pass

class GetCoordenadaCSV(GetCoordenada):
    def get_coordenada(self, ciudad):
        with open('worldcities.csv', 'r') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if fila[0] == ciudad.nombreCiudad and fila[1] == ciudad.nombrePais:
                    return Coordenada(float(fila[2]), float(fila[3]))
    
class GetCoordenadaAPI(GetCoordenada):
    def get_coordenada(self, ciudad):
        url = f"https://nominatim.openstreetmap.org/search?q={ciudad.nombreCiudad},peru&format=json"
        respuesta = requests.get(url).json()
        if respuesta:
            latitud = float(respuesta[0]['lat'])
            longitud = float(respuesta[0]['lon'])
            return Coordenada(latitud, longitud)

class GetCoordenadaMOCK(GetCoordenada):
    def get_coordenada(self, ciudad):
        return Coordenada(-12.0464, -77.0428)
    
def haversine(coord1, coord2):
    R = 6371

    lat1 = radians(coord1.latitud)
    lon1 = radians(coord1.longitud)
    lat2 = radians(coord2.latitud)
    lon2 = radians(coord2.longitud)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)*2 + cos(lat1) * cos(lat2) * sin(dlon / 2)*2
    c = 2 * asin(sqrt(a))

    return R * c


def main():
    ciudad1 = Ciudad("Peru", "Lima")
    ciudad2 = Ciudad("Peru", "Cusco")

    obtener_coordenadas = GetCoordenadaCSV()
    # obtener_coordenadas = GetCoordenadaAPI()
    # obtener_coordenadas = GetCoordenadaMOCK()

    coord1 = obtener_coordenadas.get_coordenada(ciudad1)
    coord2 = obtener_coordenadas.get_coordenada(ciudad2)

    distancia = haversine(coord1, coord2)
    print(f"La distancia entre {ciudad1.nombreCiudad} y {ciudad2.nombreCiudad} es {distancia:.2f} km")