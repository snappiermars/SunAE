import RPi.GPIO as GPIO
import time

SCL_PIN = 3  # Pin de reloj del I2C (SCL)
SDA_PIN = 2  # Pin de datos del I2C (SDA)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SCL_PIN, GPIO.OUT)
GPIO.setup(SDA_PIN, GPIO.OUT)

# Generar pulsos en el pin de reloj
for _ in range(20):
    GPIO.output(SCL_PIN, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(SCL_PIN, GPIO.LOW)
    time.sleep(0.01)

GPIO.cleanup()




