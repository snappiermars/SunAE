import smbus
import time

# Inicializar I2C
bus = smbus.SMBus(1)  # I2C en Raspberry Pi 3 usa el bus 1
address = 0x08  # Dirección I2C del Arduino (la misma que en Wire.begin en Arduino)

def send_angle(angle):
    if 0 <= angle <= 180:  # Validar que el ángulo esté dentro del rango
        bus.write_byte(address, angle)  # Enviar el ángulo como un byte
    else:
        print("Ángulo fuera de rango")

while True:
    angle = int(input("Introduce el ángulo (0-180): "))  # Leer ángulo desde la terminal
    send_angle(angle)
    time.sleep(1)  # Pausa de 1 segundo entre envíos

