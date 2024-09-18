import smbus
import time

# Inicializar I2C en el bus 1
bus = smbus.SMBus(1)  # Si usas Raspberry Pi 3 o superior, usa el bus 1
I2C_ADDRESS = 0x08  # Dirección I2C del Arduino (asegúrate de que es la correcta)

        def send_angles(angles):
    if all(0 <= angle <= 180 for angle in angles):
        try:
            bus.write_i2c_block_data(I2C_ADDRESS, 0, angles)
            print(f"Ángulos enviados: {angles}")
            
            # Leer la respuesta del Arduino para confirmar recepción
            confirmation = bus.read_byte(I2C_ADDRESS)
            if confirmation == 1:
                print("Ángulos recibidos correctamente por Arduino.")
            else:
                print("Error en la recepción de ángulos en Arduino.")
            
        except OSError as e:
            print(f"Error de comunicación: {e}")
    else:
        print("Algunos ángulos están fuera de rango. Deben estar entre 0 y 180.")

while True:
    try:
        # Pedir los ángulos de los 3 servos
        angle1 = int(input("Introduce el ángulo del servo 1 (0-180): "))
        angle2 = int(input("Introduce el ángulo del servo 2 (0-180): "))
        angle3 = int(input("Introduce el ángulo del servo 3 (0-180): "))
        
        # Crear una lista con los tres ángulos
        angles = [angle1, angle2, angle3]
        
        # Enviar los ángulos al Arduino
        send_angles(angles)
        # Pausa de 2 segundo entre envíos
        time.sleep(5)  
    except ValueError:
        print("Por favor, introduce un número válido.")

