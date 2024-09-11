import smbus
import time

bus = smbus.SMBus(1)
arduino_address = 0x08

# Envía un valor PWM al Arduino
pwm_value = 128  # Valor entre 0 y 255
bus.write_byte(arduino_address, pwm_value)
