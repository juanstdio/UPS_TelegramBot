import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Leer el archivo CSV
print("Leyendo el archivo CSV...")
df = pd.read_csv('datos.csv', parse_dates=['timestamp'])
print("Archivo CSV leído con éxito.")

# Aplicar un suavizado con media móvil
print("Aplicando suavizado con media móvil...")
df['linev_smooth'] = df['linev'].rolling(window=3, center=True).mean()
df['loadpct_smooth'] = df['loadpct'].rolling(window=3, center=True).mean()
df['battv_smooth'] = df['bcharge'].rolling(window=3, center=True).mean()
print("Suavizado aplicado.")

# Crear subplots
print("Creando gráficos...")
fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

# Formato para la fecha en el eje x
date_format = DateFormatter('%H:%M')

# Graficar linev con suavizado
axs[0].plot(df['timestamp'], df['linev_smooth'], color='blue')
axs[0].set_title('Voltaje de Línea')
axs[0].set_ylabel('Voltaje (V)')
axs[0].grid(True)
axs[0].xaxis.set_major_formatter(date_format)

# Graficar bcharge con suavizado
axs[1].plot(df['timestamp'], df['battv_smooth'], color='green')
axs[1].set_title('Carga Bateria')
axs[1].set_ylabel('Carga Bateria %')
axs[1].grid(True)
axs[1].xaxis.set_major_formatter(date_format)

# Graficar loadpct con suavizado
axs[2].plot(df['timestamp'], df['loadpct_smooth'], color='red')
axs[2].set_title('Consumo ')
axs[2].set_ylabel('Consumo (%)')
axs[2].grid(True)
axs[2].xaxis.set_major_formatter(date_format)

# Rotar las etiquetas del eje x para que no se superpongan
plt.xticks(rotation=45)

# Ajustar espacio entre subplots
plt.tight_layout()

# Guardar la imagen como PNG
print("Guardando la imagen como PNG...")
plt.savefig('chart.png', format='png')
print("Imagen guardada con éxito.")
