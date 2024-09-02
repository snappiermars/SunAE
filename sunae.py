import math #Importamos la libreria math para realizar los calculos necesarios

class SolarPosition:
    def __init__(self, year:int, day_of_year:int, hour:float, latitude:float, longitude:float): #Atributos de la clase
        self.year = year
        self.day_of_year = day_of_year
        self.hour = hour
        self.latitude = latitude
        self.longitude = longitude
        self.pi = math.pi
        self.twopi = 2 * self.pi
        self.rad = self.pi / 180
    
    def calculate_julian_day(self): #Calcula el dia juliano para la fecha actual
        delta = self.year - 1949
        leap = math.floor(delta / 4)
        jd = 32916.5 + delta * 365 + leap + self.day_of_year + self.hour / 24
        return jd

    def calculate_solar_position(self): #Calula la posicion del sol (azimut y elevacion)
        jd = self.calculate_julian_day()
        time = jd - 51545.0

        # Cálculo de la longitud media del Sol
        mnlong = 280.460 + 0.9856474 * time
        mnlong = mnlong % 360
        if mnlong < 0:
            mnlong += 360

        # Anomalía media del Sol
        mnanom = 357.528 + 0.9856003 * time
        mnanom = mnanom % 360
        if mnanom < 0:
            mnanom += 360
        mnanom = mnanom * self.rad

        # Longitud eclíptica del Sol
        eclong = mnlong + 1.915 * math.sin(mnanom) + 0.020 * math.sin(2 * mnanom)
        eclong = eclong % 360
        if eclong < 0:
            eclong += 360
        oblqec = 23.439 - 0.0000004 * time
        eclong = eclong * self.rad
        oblqec = oblqec * self.rad

        # Cálculo de ascensión recta y declinación
        num = math.cos(oblqec) * math.sin(eclong)
        den = math.cos(eclong)
        ra = math.atan2(num, den)
        if den < 0:
            ra += self.pi
        elif num < 0:
            ra += self.twopi

        dec = math.asin(math.sin(oblqec) * math.sin(eclong))

        # Cálculo del tiempo sideral en Greenwich
        gmst = 6.697375 + 0.0657098242 * time + self.hour
        gmst = gmst % 24
        if gmst < 0:
            gmst += 24

        # Tiempo local medio sideral
        lmst = gmst + self.longitude / 15
        lmst = lmst % 24
        if lmst < 0:
            lmst += 24
        lmst = lmst * 15 * self.rad

        # Cálculo del ángulo horario
        ha = lmst - ra
        if ha < -self.pi:
            ha += self.twopi
        if ha > self.pi:
            ha -= self.twopi

        # Convertir latitud a radianes
        lat = self.latitude * self.rad

        # Cálculo de la elevación
        el = math.asin(math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha))
        az = math.atan2(-math.cos(dec) * math.sin(ha), math.cos(lat) * math.sin(dec) - math.sin(lat) * math.cos(dec) * math.cos(ha))

        if az < 0:
            az += self.twopi

        # Convertir elevación a grados
        el_deg = el / self.rad
        if el_deg > -0.56:
            refrac = 3.51561 * (0.1594 + 0.0196 * el_deg + 0.00002 * el_deg**2) / (1 + 0.505 * el_deg + 0.0845 * el_deg**2)
        else:
            refrac = 0.56
        el = el_deg + refrac

        az = az / self.rad

        return az, el

# Ejemplo de uso de la clase
if __name__ == "__main__":
    # Crear una instancia de la clase con la fecha, hora y coordenadas
    solar_position = SolarPosition(2024, 242, 12.5, 19.4326, -99.1332)
    
    # Calcular la posición del sol
    azimuth, elevation = solar_position.calculate_solar_position()

    print(f"Azimut: {azimuth:.2f}°")
    print(f"Elevación: {elevation:.2f}°")
