import tkinter as tk
from tkinter import ttk
from weather import WeatherDataProcessor as wdp

# Objeto para obtener los datos del clima
clima = wdp()
clima.obtener_datos()
# Obtener la lista de estados disponibles
estados = clima.listar_estados()

# Crear la ventana principal
root = tk.Tk()
root.title("Listas Desplegables Dependientes con Tkinter")

# Crear un Label para mostrar la selección del estado
label_estado = tk.Label(root, text="Selecciona un estado:")
label_estado.pack(pady=10)

# Crear la lista desplegable (Combobox) para los estados
combobox_estado = ttk.Combobox(root, values=estados)
combobox_estado.pack(pady=10)

# Crear un Label para mostrar la selección del municipio
label_municipio = tk.Label(root, text="Selecciona un municipio:")
label_municipio.pack(pady=10)

# Crear la lista desplegable (Combobox) para los municipios
combobox_municipio = ttk.Combobox(root)
combobox_municipio.pack(pady=10)

# Crear un Label para mostrar la selección de la localidad
label_localidad = tk.Label(root, text="Selecciona una localidad:")
label_localidad.pack(pady=10)

# Crear la lista desplegable (Combobox) para las localidades
combobox_localidad = ttk.Combobox(root)
combobox_localidad.pack(pady=10)

# Crear un Label para mostrar la información de la localidad
label_info = tk.Label(root, text="")
label_info.pack(pady=10)

# Función para actualizar los municipios según el estado seleccionado
def actualizar_municipios(event):
    estado_seleccionado = combobox_estado.get()
    municipios = clima.listar_municipios(estado_seleccionado)
    combobox_municipio['values'] = municipios
    combobox_municipio.set('')  # Limpiar selección previa
    combobox_localidad['values'] = []  # Limpiar localidades previas
    label_info.config(text="")  # Limpiar información previa

# Función para actualizar las localidades según el municipio seleccionado
def actualizar_localidades(event):
    estado_seleccionado = combobox_estado.get()
    municipio_seleccionado = combobox_municipio.get()
    arlocal = clima.mostrar_datos_estado_municipio(estado_seleccionado,municipio_seleccionado)
    localidades = [f"Localidad #{i}" for i in range(len(arlocal))]  # Asumiendo que este método existe
    # Formatear localidades como "localidad #n"
    combobox_localidad['values'] = localidades
    combobox_localidad.set('')  # Limpiar selección previa
    label_info.config(text="")  # Limpiar información previa

# Función para mostrar la información de la localidad seleccionada
def mostrar_info_localidad(event):
    seleccion = combobox_localidad.get()
    estado_seleccionado = combobox_estado.get()
    municipio_seleccionado = combobox_municipio.get()
    arlocal = clima.mostrar_datos_estado_municipio(estado_seleccionado, municipio_seleccionado)
    if seleccion:
        # Extraer el número de localidad de la selección
        num_localidad = int(seleccion.split('#')[1].strip())  # Obtener el número después de "Localidad #"
        # Buscar la localidad correspondiente
        info = (
                f"Descripción del cielo: {arlocal[num_localidad]['desciel']}\n"
                f"Temperatura máxima: {arlocal[num_localidad]['tmax']}°C\n"
                f"Temperatura mínima: {arlocal[num_localidad]['tmin']}°C\n"
                f"Probabilidad de precipitación: {arlocal[num_localidad]['probprec']}%\n"
                f"Ráfagas: {arlocal[num_localidad]['raf']} km/h\n"
                f"Dirección del viento: {arlocal[num_localidad]['dirvienc']} ({arlocal[num_localidad]['dirvieng']}°)\n"
                f"Latitud: {arlocal[num_localidad]['lat']}, Longitud: {arlocal[num_localidad]['lon']}"
                )
        label_info.config(text=info)

# Asociar la función de actualización de municipios al evento de selección del estado
combobox_estado.bind("<<ComboboxSelected>>", actualizar_municipios)

# Asociar la función de actualización de localidades al evento de selección del municipio
combobox_municipio.bind("<<ComboboxSelected>>", actualizar_localidades)

# Asociar la función para mostrar información de la localidad seleccionada
combobox_localidad.bind("<<ComboboxSelected>>", mostrar_info_localidad)

# Iniciar el loop de la aplicación
root.mainloop()
