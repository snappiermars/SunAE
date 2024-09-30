# -*- coding: utf-8 -*-

# Importamos la librer�a necesaria
from adafruit_servokit import ServoKit
import time

# Inicializamos la placa PCA9685 con 16 canales
kit = ServoKit(channels=16)
servo=1

# Configuramos el �ngulo m�ximo y m�nimo del servomotor
min_angle = 0
max_angle = 0.5

# Control de un servomotor en el canal 0
servo_channel = 0

def mover_servomotor(angulo):
    # Limitamos el �ngulo al rango permitido
    if angulo < min_angle:
        angulo = min_angle
    elif angulo > max_angle:
        angulo = max_angle

    # Movemos el servomotor al �ngulo especificado
    kit.servo[servo_channel].angle = angulo
    print(f"Moviendo el servomotor a {angulo} grados")
    time.sleep(1)

# Ejemplo de movimiento
if __name__ == "__main__":
    try:
        while True:
            # Mover el servomotor al �ngulo m�nimo
            mover_servomotor(min_angle)
            # Mover el servomotor al �ngulo m�ximo
            mover_servomotor(max_angle)
    except KeyboardInterrupt:
        print("Programa detenido")
