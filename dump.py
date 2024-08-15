import mysql.connector
from datetime import datetime
import csv

# Conexión a la base de datos
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='bob',
    password='alice',
    database='testdb'
)

cursor = conn.cursor()

# Obteniendo los nombres de las columnas de la tabla
cursor.execute("SHOW COLUMNS FROM apc")
columns = cursor.fetchall()
column_names = [column[0] for column in columns]

# Construyendo la consulta para obtener todas las columnas y las últimas 200 filas ordenadas por id(osea, el ingreso en la tabla)
query = "SELECT * FROM apc ORDER BY id DESC LIMIT 200"
print("dumping from db")
# Ejecutando la consulta
cursor.execute(query)
rows = cursor.fetchall()

# Guardando el resultado en un archivo .csv con fecha y hora
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_name = f"datos.csv"

# Escribiendo en el archivo CSV
with open(file_name, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Escribir los nombres de las columnas
    writer.writerow(column_names)
    # Escribir las filas
    writer.writerows(rows)

# Cerrar la conexión
cursor.close()
print("csv dumped, saving!")
conn.close()
