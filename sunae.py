import math

class SolarPosition:
    def __init__(self, year, day_of_year, latitude, longitude):
        self.year = year
        self.day_of_year = day_of_year
        self.latitude = latitude
        self.longitude = longitude
        self.pi = math.pi
        self.twopi = 2 * self.pi
        self.rad = self.pi / 180

    def calculate_julian_day(self, hour):
        """Calcula el día juliano para la fecha actual con la hora proporcionada."""
        delta = self.year - 1949
        leap = math.floor(delta / 4)
        jd = 32916.5 + delta * 365 + leap + self.day_of_year + hour / 24
        return jd

    def calculate_solar_position(self, hour):
        """Calcula la posición solar (azimut y elevación) basada en la fecha, hora y coordenadas."""
        jd = self.calculate_julian_day(hour)
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
        gmst = 6.697375 + 0.0657098242 * time + hour
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

    def calculate_daily_trajectory(self):
        """Calcula la trayectoria del Sol para cada hora de un día dado."""
        azimuths = []
        elevations = []
        
        for hour in range(0, 24):
            az, el = self.calculate_solar_position(hour)
            azimuths.append(az)
            elevations.append(el)
        
        return azimuths, elevations

# Ejemplo de uso de la clase
if __name__ == "__main__":
    # Crear una instancia de la clase con la fecha y coordenadas
    solar_position = SolarPosition(2024, 242, 19.4326, -99.1332)
    
    # Calcular la trayectoria del sol a lo largo del día
    azimuths, elevations = solar_position.calculate_daily_trajectory()

    # Mostrar los resultados
    print("Trayectoria del Sol durante el día:")
    for hour, (az, el) in enumerate(zip(azimuths, elevations)):
        print(f"Hora: {hour:02d}:00 - Azimut: {az:.2f}°, Elevación: {el:.2f}°")

