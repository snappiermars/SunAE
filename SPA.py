import math
from datetime import datetime, timedelta

class SolarCalculator:
    def __init__(self, latitude, longitude, elevation, timezone):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.timezone = timezone

    def julian_day(self, dt):
        """Cálculo del Día Juliano para una fecha dada."""
        year, month, day, hour, minute, second = dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        jd = (367 * year) - math.floor(7 * (year + math.floor((month + 9) / 12)) / 4) + \
             math.floor(275 * month / 9) + day + 1721013.5 + \
             (hour + minute / 60 + second / 3600 - self.timezone) / 24
        return jd

    def solar_position(self, dt):
        """Cálculo de la posición solar para una fecha y hora específicas."""
        jd = self.julian_day(dt)
        jc = (jd - 2451545) / 36525

        # Cálculo de variables intermedias
        l0 = (280.46646 + jc * (36000.76983 + jc * 0.0003032)) % 360
        m = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)
        e = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)
        c = math.sin(math.radians(m)) * (1.914602 - jc * (0.004817 + 0.000014 * jc)) + \
            math.sin(math.radians(2 * m)) * (0.019993 - 0.000101 * jc) + \
            math.sin(math.radians(3 * m)) * 0.000289
        sun_true_long = l0 + c
        omega = 125.04 - 1934.136 * jc
        sun_app_long = sun_true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
        epsilon0 = 23 + (26 + ((21.448 - jc * (46.815 + jc * (0.00059 - jc * 0.001813)))) / 60) / 60
        epsilon = epsilon0 + 0.00256 * math.cos(math.radians(omega))

        # Cálculo de la ascensión recta y declinación del Sol
        alpha = math.degrees(math.atan2(math.cos(math.radians(epsilon)) * math.sin(math.radians(sun_app_long)),
                                        math.cos(math.radians(sun_app_long))))
        delta = math.degrees(math.asin(math.sin(math.radians(epsilon)) * math.sin(math.radians(sun_app_long))))

        # Cálculo de la hora solar y las horas de amanecer/atardecer
        h = (math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(math.radians(self.latitude)) * math.cos(math.radians(delta))) -
                                   math.tan(math.radians(self.latitude)) * math.tan(math.radians(delta)))))

        solar_noon = (720 - 4 * self.longitude - h) / 1440
        sunrise_time = solar_noon - h / 360
        sunset_time = solar_noon + h / 360

        return {
            'Julian Day': jd,
            "Sun's Declination": delta,
            'Right Ascension': alpha,
            'Sunrise (UTC)': sunrise_time * 24,
            'Sunset (UTC)': sunset_time * 24,
            'Solar Noon (UTC)': solar_noon * 24
        }

    def calculate_day_trajectory(self, date):
        """Calcula la trayectoria solar completa para un día específico (en intervalos de 10 minutos)."""
        time_interval = timedelta(minutes=10)  # Intervalo de 10 minutos
        times = []
        solar_positions = []

        # Inicializa el tiempo en la medianoche
        dt = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_time = dt + timedelta(days=1)  # Termina en la medianoche del día siguiente

        while dt < end_time:
            position = self.solar_position(dt)
            times.append(dt)
            solar_positions.append({
                'time': dt,
                'declination': position["Sun's Declination"],
                'right_ascension': position['Right Ascension'],
                'sunrise': position['Sunrise (UTC)'],
                'sunset': position['Sunset (UTC)'],
                'solar_noon': position['Solar Noon (UTC)']
            })
            dt += time_interval

        return solar_positions
if __name__ == "__main__":
    # Parámetros de la Ciudad de México
    latitude = 19.4326  # Latitud de Ciudad de México
    longitude = -99.1332  # Longitud de Ciudad de México
    elevation = 2240  # Elevación en metros
    timezone = -6  # Zona horaria UTC-6

    # Crear una instancia de SolarCalculator para la Ciudad de México
    solar_calculator = SolarCalculator(latitude, longitude, elevation, timezone)

    # Fecha específica para la cual queremos calcular la trayectoria solar
    date = datetime(2024, 10, 6)  # 6 de octubre de 2024

    # Calcular la trayectoria solar para todo el día, en intervalos de 10 minutos
    trajectory = solar_calculator.calculate_day_trajectory(date)

    # Imprimir resultados
    for point in trajectory:
        print(f"Hora: {point['time'].strftime('%Y-%m-%d %H:%M:%S')}, "
            f"Declinación: {point['declination']:.2f}°, "
            f"Ascension: {point['right_ascension']:.2f}"
            f"Amanecer (UTC): {point['sunrise']:.2f}, "
            f"Atardecer (UTC): {point['sunset']:.2f}, "
            f"Mediodía Solar (UTC): {point['solar_noon']:.2f}")

