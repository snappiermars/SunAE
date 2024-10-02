import tkinter as tk
from datetime import datetime
from sunae import SolarPosition  # Asegúrate de que el archivo con la clase se llama `solar_position.py`
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from adafruit_servokit import ServoKit
import time

# Variables globales para la actualización
actualizando_posicion = False

def calcular_posicion_actual():
    """Calcula y actualiza la posición actual del Sol en la etiqueta y gráfica."""
    global actualizando_posicion
    if actualizando_posicion:  # Verificar si ya se está actualizando
        return

    actualizando_posicion = True

    # Obtener la fecha y la hora actual
    now = datetime.now()
    year = now.year
    day_of_year = now.timetuple().tm_yday
    hour = now.hour + now.minute / 60.0

    # Coordenadas de ejemplo (Ciudad de México)
    latitude = 19.4326
    longitude = -99.1332

    # Crear una instancia de la clase SolarPosition
    solar = SolarPosition(year, day_of_year, latitude, longitude)

    # Calcular la posición del Sol
    azimuth, elevation = solar.calculate_solar_position(hour)

    # Mostrar los resultados en la etiqueta
    resultado_posicion.config(text=f"Azimut: {azimuth:.2f}°\nElevación: {elevation:.2f}°")

    # Actualizar la gráfica con la posición actual
    plot_solar_position(azimuth, elevation)

    # Programar la siguiente actualización en 1000 ms (1 segundo)
    ventana.after(1000, calcular_posicion_actual)
    actualizando_posicion = False

def calcular_trayectoria():
    """Calcula la trayectoria diaria del Sol y la grafica en la interfaz."""
    # Obtener la fecha actual
    now = datetime.now()
    year = now.year
    day_of_year = now.timetuple().tm_yday

    # Coordenadas de ejemplo (Ciudad de México)
    latitude = 19.4326
    longitude = -99.1332

    # Crear una instancia de la clase SolarPosition
    solar = SolarPosition(year, day_of_year, latitude, longitude)

    # Calcular la trayectoria diaria
    azimuths, elevations = solar.calculate_daily_trajectory()

    # Mostrar los resultados en la etiqueta
    result = "\n".join([f"Hora {i}: Azimut: {azimuths[i]:.2f}°, Elevación: {elevations[i]:.2f}°" for i in range(24)])
    resultado_trayectoria.config(text=result)

    # Graficar la trayectoria del Sol
    plot_solar_trajectory(azimuths, elevations)

def plot_solar_position(azimuth, elevation):
    """Actualiza la gráfica en tiempo real con la posición actual del Sol."""
    global ax, canvas

    # Limpiar la gráfica actual completamente
    ax.clear()

    # Convertir el ángulo de azimut de grados a radianes para la gráfica polar
    azimuth_rad = azimuth * math.pi / 180

    # Graficar la posición actual del Sol
    ax.plot(azimuth_rad, elevation, 'ro', label="Posición Actual del Sol")
    
    # Configurar la orientación y dirección de los ángulos en el gráfico polar
    ax.set_theta_zero_location('N')  # Establece el norte (0°) en la parte superior de la gráfica
    ax.set_theta_direction(-1)  # Configura la dirección de los ángulos en sentido horario
    ax.set_ylim(0, 90)  # Limitar el rango de la elevación de 0 a 90 grados

    # Actualizar la gráfica
    ax.legend(loc="upper right")
    canvas.draw()

def plot_solar_trajectory(azimuths, elevations):
    """Grafica la trayectoria del Sol durante el día en una gráfica polar."""
    global ax, canvas

    # Limpiar la gráfica actual completamente
    ax.clear()

    # Convertir los ángulos de azimut de grados a radianes para la gráfica polar
    azimuths_rad = [az * math.pi / 180 for az in azimuths]

    # Convertir a arrays numpy para mejor manipulación
    azimuths_rad = np.array(azimuths_rad)
    elevations = np.array(elevations)

    # Filtrar elevaciones negativas y azimuths correspondientes
    valid_indices = elevations > 0  # Consideramos solo elevaciones positivas
    azimuths_rad = azimuths_rad[valid_indices]
    elevations = elevations[valid_indices]

    if len(elevations) == 0:
        print("No hay datos válidos para graficar.")
        return

    # Usar un gradiente de color para la trayectoria del Sol (colores cálidos para mayor elevación)
    scatter = ax.scatter(azimuths_rad, elevations, c=elevations, cmap='plasma', s=50, edgecolor='black', label="Trayectoria del Sol")

    # Añadir una barra de color para indicar la elevación
    ax.figure.colorbar(scatter, ax=ax, orientation='vertical').set_label('Elevación (grados)', fontsize=12)

    # Configurar la orientación y dirección de los ángulos en el gráfico polar
    ax.set_theta_zero_location('N')  # Establece el norte (0°) en la parte superior de la gráfica
    ax.set_theta_direction(-1)  # Configura la dirección de los ángulos en sentido horario
    ax.set_ylim(0, 90)  # Limitar el rango de la elevación de 0 a 90 grados

    # Añadir título y leyenda a la gráfica
    ax.set_title('Trayectoria del Sol durante el Día', fontsize=14)
    ax.legend(loc="upper right")

    # Actualizar la gráfica
    canvas.draw()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Posición Solar")

# Crear una figura para la gráfica polar
fig = plt.Figure(figsize=(5, 5))
ax = fig.add_subplot(111, polar=True)

# Incrustar la figura en la ventana de tkinter
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack()

# Crear los botones
boton_posicion = tk.Button(ventana, text="Calcular Posición Actual del Sol", command=calcular_posicion_actual)
boton_posicion.pack(pady=10)

boton_trayectoria = tk.Button(ventana, text="Calcular Trayectoria del Sol", command=calcular_trayectoria)
boton_trayectoria.pack(pady=10)

# Crear etiquetas para mostrar los resultados
resultado_posicion = tk.Label(ventana, text="", justify=tk.LEFT, padx=10, pady=10)
resultado_posicion.pack()

resultado_trayectoria = tk.Label(ventana, text="", justify=tk.LEFT, padx=10, pady=10)
resultado_trayectoria.pack()

# Ejecutar la ventana principal
ventana.mainloop()
print("HOLA DESDE EL CUBICULOs")