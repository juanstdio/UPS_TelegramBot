
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com) [![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org/)

![GitHub repo size](https://img.shields.io/github/repo-size/juanstdio/UPS_TelegramBot)![GitHub license](https://img.shields.io/github/license/juanstdio/UPS_TelegramBot)
![amd64-shield](https://img.shields.io/badge/amd64-yes-green.svg)![armhf-shield](https://img.shields.io/badge/armhf-yes-green.svg)![armv7-shield](https://img.shields.io/badge/armv7-yes-green.svg)![i386-shield](https://img.shields.io/badge/i386-yes-green.svg)

### Expansión del Proyecto del Bot

### Problema Inicial

Hasta ahora, el bot estaba diseñado para mostrar siempre información en tiempo real cada vez que se realizaba una consulta. Sin embargo, vi la oportunidad de agregar nuevas capacidades que no solo respondieran consultas en tiempo real, sino que también trabajaran con datos almacenados para un análisis más profundo.

### Integración con Base de Datos MariaDB (MySQL)

En paralelo, comencé a experimentar con una base de datos MariaDB (MySQL), donde creé una tabla llamada `apcaccess`. Esta tabla almacena varios valores clave de la UPS, que son fundamentales para generar gráficas útiles y para realizar prácticas con otras bibliotecas de análisis de datos.

La base de datos creció rápidamente, lo que me permitió implementar una API utilizando FastAPI, gracias a la guía de [Juan Gonzalez](https://github.com/juanchixd).

### API de Consultas a la Base de Datos

La API cuenta con un método simple pero útil llamado `last_ups_data`, disponible en `/api/last_ups_data`. Este método realiza una consulta SQL a la tabla `apcaccess` y devuelve el último valor registrado, basado en el ID de la tabla. Puedes encontrar más detalles en la [documentación de la API](https://github.com/juanchixd/Bot_ups_Lyonn/blob/main/README.MD#api).


### En Python

#### Instalar los paquetes requeridos para la conexión SQL

(Estamos asumiendo que hay una instalación de Python3.11 con el gestor de Paquetes PIP)

```bash
pip install requests mysql-connector-python fastapi[standard] uvicorn[standard]
```

### Explicación de la funcion last_ups_data
La función `last_ups_data` se encarga de obtener el último registro de datos de la tabla `apcaccess` en una base de datos MySQL. A continuación se describe su funcionamiento:
el host `xxx.yyy.xxx.yyy` es la dirección IP donde la base de datos está funcionando,
el parámetro `database` es totalmente arbitrario y debe ser redifinido para cada caso en particular. 


```python
def last_ups_data():
    conn = mysql.connector.connect(host='xxx.yyy.xxx.yyy',user='xtz123',password='213456',database='changeme')
    cursor = conn.cursor()
    query = "SELECT * FROM apcaccess ORDER BY id DESC LIMIT 1"
    data = ""
    print("dumping from db")
    cursor.execute(query)
    rows = cursor.fetchall()
    rows = str(rows[0]).split(",")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    data = {
        "timestamp": timestamp,
        "linev": float(rows[7].strip()),
        "battv": float(rows[11].split(')')[0].strip()),
        "loadpct": float(rows[10].strip()),
        "battery_charge": float(rows[8].strip()),
        "timeleft": float(rows[9].strip())
    }
    cursor.close()
    conn.close()
    return data if data else HTTPException(
        status_code=404, detail="No se encontraron registros")
```

1. **Conexión a la Base de Datos**: La función establece una conexión con la base de datos `masterdb` utilizando las credenciales proporcionadas.

2. **Consulta SQL**: Ejecuta una consulta SQL que selecciona el registro más reciente (`ORDER BY id DESC LIMIT 1`).

3. **Procesamiento de Datos**: El resultado de la consulta se convierte en una lista de valores, de la cual se extraen y formatean campos clave como voltaje de línea (`linev`), voltaje de batería (`battv`), porcentaje de carga (`loadpct`), nivel de carga de la batería (`battery_charge`), y tiempo restante (`timeleft`).

4. **Formateo del Timestamp**: La función también incluye un timestamp con precisión en milisegundos para marcar el momento en que se generaron los datos.

5. **Respuesta**: Devuelve un diccionario con los valores formateados. Si no se encuentra ningún registro, la función lanza una excepción HTTP 404.

Esta función es crucial para obtener rápidamente el estado actual de la UPS y puede integrarse fácilmente en sistemas que requieran monitoreo en tiempo real.

## Gratitudes
- **Juan Gonzalez** & **Eze Fernandez** - _Por la mano y el feedback_ - [Juan Gonzalez](https://github.com/juanchixd) - [Eze Fernandez](https://github.com/ezefernandez93)

## Licencia

Apache 2.0 - see the [LICENSE](LICENSE) 

```python
# API UPS - Developed by Juan Blanc / Juan Gonzalez / Ezequiel Fernandez
# Just for Fun!
```
