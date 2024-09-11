import smbus
import time

# Inicializar I2C en el bus 1
bus = smbus.SMBus(1)  # I2C en Raspberry Pi 3 usa el bus 1
I2C_ADDRESS= 0x08  # Dirección I2C del Arduino (la misma que en Wire.begin en Arduino)

def send_angle(angle):
    if 0 <= angle <= 180:  # Validar que el ángulo esté dentro del rango
        try:
            bus.write_byte(I2C_ADDRESS, angle)  # Enviar el ángulo como un byte
            print(f"Ángulo enviado: {angle}")
        except OSError as e:
            print(f"Error de comunicación: {e}")
    else:
        print("Ángulo fuera de rango. Debe estar entre 0 y 180.")

while True:
    try:
        angle = int(input("Introduce el ángulo (0-180): "))  # Leer ángulo desde la terminal
        send_angle(angle)
        time.sleep(1)  # Pausa de 1 segundo entre envíos
    except ValueError:
        print("Por favor, introduce un numero valido.")

