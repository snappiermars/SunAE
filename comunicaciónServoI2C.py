import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Inicializa I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inicializa el primer PCA9685 en la dirección I2C 0x40 (por defecto)
pca1 = PCA9685(i2c, address=0x40)
pca1.frequency = 50  # Frecuencia para servos

# Inicializa el segundo PCA9685 en la dirección I2C 0x41
pca2 = PCA9685(i2c, address=0x41)
pca2.frequency = 50  # Frecuencia para servos

# Crea objetos Servo para el primer PCA9685 (canales 0-15)
servos_pca1 = [servo.Servo(pca1.channels[i]) for i in range(16)]

# Crea objetos Servo para el segundo PCA9685 (canales 0-13)
servos_pca2 = [servo.Servo(pca2.channels[i]) for i in range(14)]

# Función para mover todos los servos
def mover_todos_los_servos():
    # Mueve servos en PCA1
    for i, servo_motor in enumerate(servos_pca1):
        servo_motor.angle = 90  # Mover a 90 grados
        print(f"Servo {i} en PCA1 movido a 90 grados")
        time.sleep(0.1)
    
    # Mueve servos en PCA2
    for i, servo_motor in enumerate(servos_pca2):
        servo_motor.angle = 90  # Mover a 90 grados
        print(f"Servo {i} en PCA2 movido a 90 grados")
        time.sleep(0.1)

try:
    mover_todos_los_servos()

except KeyboardInterrupt:
    print("Programa interrumpido")

finally:
    pca1.deinit()
    pca2.deinit()



