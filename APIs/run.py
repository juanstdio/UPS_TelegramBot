
import uvicorn
from fastapi import FastAPI, HTTPException
import mysql.connector
from datetime import datetime

tags_metadata = [
    {
        "name": "Hello World",
        "description": "Saludar al mundo",
    },
    {
        "name": "UPS",
        "description": "Obtener el estado de la UPS",
    },
]


app = FastAPI(
    title="APC UPS API",
    description="API  UPS APC 1500VA",
    version="1.0.3",
    contact={
        "name": "Juan Blanc",
        "email": "juan@blanc.com.ar",
    },
    license_info={
        "name": "Apache2",
        "identifier": "Apache2.0",
        "url": "https://opensource.org/license/apache-2-0",
    },
    openapi_tags=tags_metadata,
)


@app.get("/", tags=["Hello World"])
async def root():
    return {"message": "Hello World"}


@app.get("/api/last_ups_data", tags=["UPS"], responses={
    200: {
        "description": "Response",
        "content": {
            "application/json": {
                "example": {
                    "timestamp": "2024-08-15 19:10:50",
                    "battery_charge": 100,
                    "timeleft": 21.5,
                    "loadpct": 10,
                    "linev": 231,
                    "battv": 27.3
                }
            }
        }
    },
    404: {
        "description": "No se encontraron registros",
        "content": {
            "application/json": {
                "example": {"detail": "No se encontraron registros"}
            }
        }
    }
})
def last_ups_data():
    # Obtiene el último registro
    conn = mysql.connector.connect(host='xxx.yyy.xxx.yyy',user='xtz123',password='213456',database='masterdb')
    cursor = conn.cursor()
    query = "SELECT * FROM apcaccess ORDER BY id DESC LIMIT 1"
    data = ""
    print("dumping from db")
    # Ejecutando la consulta
    cursor.execute(query)
    rows = cursor.fetchall()
    rows = str(rows[0]).split(",")
    # Formateando la fecha y hora en el formato deseado
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # Creando un diccionario con los datos formateados
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

def main():
    uvicorn.run(app, host="0.0.0.0", port=5005)


if __name__ == "__main__":
    main()
