# -*- coding: utf-8 -*-

# Importamos la librería necesaria
from adafruit_servokit import ServoKit
import time
import math
import sunae

# Inicializamos la placa PCA9685 con 16 canales
kit = ServoKit(channels=16)
servo=1

# Configuramos el ángulo máximo y mínimo del servomotor
#min_angle = 0
#max_angle = 180

# Control de un servomotor en el canal 0
servo_channel = 0

def mover_servomotor(angulo):
    # Limitamos el ángulo al rango permitido
    if angulo < 0:
        angulo = 0
    elif angulo > 180:
        angulo = 180

    # Movemos el servomotor al ángulo especificado
    kit.servo[servo_channel].angle = angulo
    print(f"Moviendo el servomotor a {angulo} grados")
    time.sleep(1)

# Ejemplo de movimiento
if __name__ == "__main__":
    try:
        while True:
            # Mover el servomotor al ángulo mínimo
            mover_servomotor(azimuths)
            # Mover el servomotor al ángulo máximo
            mover_servomotor(azimuths)
    except KeyboardInterrupt:
        print("Programa detenido")
