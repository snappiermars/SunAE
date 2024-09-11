import smbus
import time

# Dirección I2C del esclavo (Arduino Mega)
I2C_ADDRESS = 0x08

# Crear objeto para usar I2C
bus = smbus.SMBus(1)

def send_message(message):
    try:
        # Convertir el mensaje a lista de bytes y enviar al esclavo
        bus.write_i2c_block_data(I2C_ADDRESS, 0, [ord(c) for c in message])
        print(f"Mensaje enviado: {message}")
    except OSError as e:
        print(f"Error enviando mensaje: {e}")

while True:
    mensaje = input("Escribe el mensaje para enviar al Arduino: ")
    send_message(mensaje)
    time.sleep(1)  # Pausar un momento antes de enviar el siguiente mensaje
