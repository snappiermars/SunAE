import math
from datetime import datetime

def spa(year, month, day, hour, minute, second, timezone, latitude, longitude, elevation):
    # Julian day calculation
    jd = (367 * year) - math.floor(7 * (year + math.floor((month + 9) / 12)) / 4) + math.floor(275 * month / 9) + day + 1721013.5 + (hour + minute / 60 + second / 3600 - timezone) / 24

    # Julian century
    jc = (jd - 2451545) / 36525

    # Geometric mean longitude of the sun
    l0 = (280.46646 + jc * (36000.76983 + jc * 0.0003032)) % 360

    # Geometric mean anomaly of the sun
    m = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)

    # Eccentricity of Earth's orbit
    e = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)

    # Sun's equation of center
    c = math.sin(math.radians(m)) * (1.914602 - jc * (0.004817 + 0.000014 * jc)) + math.sin(math.radians(2 * m)) * (0.019993 - 0.000101 * jc) + math.sin(math.radians(3 * m)) * 0.000289

    # True longitude of the sun
    sun_true_long = l0 + c

    # Apparent longitude of the sun
    omega = 125.04 - 1934.136 * jc
    sun_app_long = sun_true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))

    # Mean obliquity of the ecliptic
    epsilon0 = 23 + (26 + ((21.448 - jc * (46.815 + jc * (0.00059 - jc * 0.001813)))) / 60) / 60

    # Corrected obliquity of the ecliptic
    epsilon = epsilon0 + 0.00256 * math.cos(math.radians(omega))

    # Sun's right ascension
    alpha = math.degrees(math.atan2(math.cos(math.radians(epsilon)) * math.sin(math.radians(sun_app_long)), math.cos(math.radians(sun_app_long))))

    # Sun's declination
    delta = math.degrees(math.asin(math.sin(math.radians(epsilon)) * math.sin(math.radians(sun_app_long))))

    # Observer's local hour angle
    h = (math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(math.radians(latitude)) * math.cos(math.radians(delta))) - math.tan(math.radians(latitude)) * math.tan(math.radians(delta)))))

    # Solar noon (in fractional hours)
    solar_noon = (720 - 4 * longitude - h) / 1440

    # Sunrise and sunset (in fractional hours)
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

# Ejemplo de uso
latitude = 40.7128  # latitud de Nueva York
longitude = -74.0060  # longitud de Nueva York
elevation = 10  # elevación en metros
timezone = -5  # Zona horaria UTC-5

now = datetime.now()
spa_results = spa(now.year, now.month, now.day, now.hour, now.minute, now.second, timezone, latitude, longitude, elevation)

print(spa_results)
