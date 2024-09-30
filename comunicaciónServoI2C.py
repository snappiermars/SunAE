# -*- coding: utf-8 -*-
from adafruit_servokit import ServoKit
import time

# Inicializamos la placa PCA9685 con 16 canales
kit = ServoKit(channels=16)

# Configuramos el ángulo máximo y mínimo del servomotor
min_angle = 0
max_angle = 180

# Control de un servomotor en el canal 0
servo_channel = 0

def mover_servomotor(angulo):
    # Limitamos el ángulo al rango permitido
    if angulo < min_angle:
        angulo = min_angle
    elif angulo > max_angle:
        angulo = max_angle

    # Movemos el servomotor al ángulo especificado
    kit.servo[servo_channel].angle = angulo
    print(f"Moviendo el servomotor a {angulo} grados")
    time.sleep(1)

# Programa principal
if __name__ == "__main__":
    try:
        while True:
            # Solicitamos el ángulo al usuario
            angulo_usuario = input(f"Ingresa el ángulo entre {min_angle} y {max_angle} grados (o 'q' para salir):")
            if angulo_usuario.lower() == 'q':
                print("Saliendo del programa")
                break
            else:
                try:
                    # Convertimos el valor ingresado a un número entero
                    angulo = int(angulo_usuario)
                    # Movemos el servomotor al ángulo especificado
                    mover_servomotor(angulo)
                except ValueError:
                    print("Por favor, ingresa un número válido")
    except KeyboardInterrupt:
        print("Programa detenido")
