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

def par_ciudades_mas_cercanas(ciudad1, ciudad2, ciudad3, obtener_coordenadas): # Nuevo método con 3 ciudades
    coord1 = obtener_coordenadas.get_coordenada(ciudad1)
    coord2 = obtener_coordenadas.get_coordenada(ciudad2)
    coord3 = obtener_coordenadas.get_coordenada(ciudad3)

    if not coord1 or not coord2 or not coord3:
        return None

    distancia1_2 = haversine(coord1, coord2)
    distancia1_3 = haversine(coord1, coord3)
    distancia2_3 = haversine(coord2, coord3)

    distancias = {
        (ciudad1.ciudad, ciudad2.ciudad): distancia1_2,
        (ciudad1.ciudad, ciudad3.ciudad): distancia1_3,
        (ciudad2.ciudad, ciudad3.ciudad): distancia2_3
    }

    par_mas_cercano = min(distancias, key=distancias.get)
    return par_mas_cercano

def main():
    ciudad1 = Ciudad("Peru", "Lima")
    ciudad2 = Ciudad("Peru", "Cusco")
    ciudad3 = Ciudad("Peru", "Arequipa")

    obtener_coordenadas = GetCoordenadaCSV()
    # obtener_coordenadas = GetCoordenadaAPI()
    # obtener_coordenadas = GetCoordenadaMOCK()

    par_cercano = par_ciudades_mas_cercanas(ciudad1, ciudad2, ciudad3, obtener_coordenadas)
    if par_cercano:
        print(f"El par de ciudades más cercano es: {par_cercano[0]} y {par_cercano[1]}.")
    else:
        print("No se pudieron obtener las coordenadas de alguna de las ciudades.")

if __name__ == "__main__":
    main()
