import math
import RPi.GPIO as GPIO
import time
import datetime
import tkinter as tk

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configuración de los pines de los servos
SERVO1_PIN = 17  # Pin del servo 1
SERVO2_PIN = 27  # Pin del servo 2

GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

# Configuración de los servos
pwm1 = GPIO.PWM(SERVO1_PIN, 50)  # Frecuencia de 50Hz
pwm2 = GPIO.PWM(SERVO2_PIN, 50)  # Frecuencia de 50Hz
pwm1.start(0)  # Inicializar en 0% de ciclo de trabajo
pwm2.start(0)  # Inicializar en 0% de ciclo de trabajo

# Función para calcular la posición del Sol
def sunae(year, day, hour, lat, long):
    pi = math.pi
    twopi = 2 * pi
    rad = pi / 180

    delta = year - 1949
    leap = math.floor(delta / 4)
    jd = 32916.5 + delta * 365 + leap + day + hour / 24

    time = jd - 51545.0

    mnlong = 280.460 + 0.9856474 * time
    mnlong = mnlong % 360
    if mnlong < 0:
        mnlong += 360

    mnanom = 357.528 + 0.9856003 * time
    mnanom = mnanom % 360
    if mnanom < 0:
        mnanom += 360
    mnanom = mnanom * rad

    eclong = mnlong + 1.915 * math.sin(mnanom) + 0.020 * math.sin(2 * mnanom)
    eclong = eclong % 360
    if eclong < 0:
        eclong += 360
    oblqec = 23.439 - 0.0000004 * time
    eclong = eclong * rad
    oblqec = oblqec * rad

    num = math.cos(oblqec) * math.sin(eclong)
    den = math.cos(eclong)
    ra = math.atan2(num, den)
    if den < 0:
        ra += pi
    elif num < 0:
        ra += twopi

    dec = math.asin(math.sin(oblqec) * math.sin(eclong))

    gmst = 6.697375 + 0.0657098242 * time + hour
    gmst = gmst % 24
    if gmst < 0:
        gmst += 24

    lmst = gmst + long / 15
    lmst = lmst % 24
    if lmst < 0:
        lmst += 24
    lmst = lmst * 15 * rad

    ha = lmst - ra
    if ha < -pi:
        ha += twopi
    if ha > pi:
        ha -= twopi

    lat = lat * rad

    el = math.asin(math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha))
    az = math.atan2(-math.cos(dec) * math.sin(ha), math.cos(lat) * math.sin(dec) - math.sin(lat) * math.cos(dec) * math.cos(ha))

    if az < 0:
        az += twopi

    el_deg = el / rad
    if el_deg > -0.56:
        refrac = 3.51561 * (0.1594 + 0.0196 * el_deg + 0.00002 * el_deg**2) / (1 + 0.505 * el_deg + 0.0845 * el_deg**2)
    else:
        refrac = 0.56
    el = el_deg + refrac

    az = az / rad

    return az, el

# Función para convertir ángulo a ciclo de trabajo del servo
def angle_to_pwm(angle):
    min_angle = 0  # Ángulo mínimo
    max_angle = 180  # Ángulo máximo
    min_pwm = 5  # Ciclo de trabajo mínimo en porcentaje
    max_pwm = 10  # Ciclo de trabajo máximo en porcentaje
    return min_pwm + (angle - min_angle) * (max_pwm - min_pwm) / (max_angle - min_angle)

# Función para actualizar la posición de los servos
def update_servos():
    # Obtener la fecha y hora actual
    now = datetime.datetime.utcnow()

    # Convertir la fecha actual a formato necesario
    year = now.year
    day_of_year = now.timetuple().tm_yday
    hour = now.hour + now.minute / 60 + now.second / 3600  # Hora en UTC decimal

    # Latitud y longitud de Ciudad de México
    lat = 19.4326  # Latitud de Ciudad de México
    long = -99.1332  # Longitud de Ciudad de México

    # Calcular la posición actual del Sol
    az, el = sunae(year, day_of_year, hour, lat, long)

    # Convertir ángulos para servos
    servo1_angle = (el + 90) % 180
    servo2_angle = az * 180 / math.pi

    # Convertir ángulos a ciclos de trabajo del servo
    servo1_pwm = angle_to_pwm(servo1_angle)
    servo2_pwm = angle_to_pwm(servo2_angle)

    # Aplicar ciclo de trabajo a los servos
    pwm1.ChangeDutyCycle(servo1_pwm)
    pwm2.ChangeDutyCycle(servo2_pwm)

    # Actualizar etiquetas en la GUI
    az_label.config(text=f"Azimut: {az * 180 / math.pi:.2f}°")
    el_label.config(text=f"Elevación: {el:.2f}°")
    
    # Programar la próxima actualización
    root.after(60000, update_servos)  # Actualizar cada minuto

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Control de Servomotores con la Posición del Sol")

# Etiquetas para mostrar la posición del Sol
az_label = tk.Label(root, text="Azimut: 0.00°", font=("Helvetica", 16))
az_label.pack(pady=10)

el_label = tk.Label(root, text="Elevación: 0.00°", font=("Helvetica", 16))
el_label.pack(pady=10)

# Iniciar la actualización de servos
update_servos()

# Ejecutar la GUI
root.mainloop()

# Limpiar GPIO al cerrar la aplicación
pwm1.stop()
pwm2.stop()
GPIO.cleanup()
