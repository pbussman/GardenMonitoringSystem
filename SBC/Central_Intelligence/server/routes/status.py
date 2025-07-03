from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3

router = APIRouter()

class SensorData(BaseModel):
    zone: str
    readings: dict

@router.get("/{zone}", response_model=SensorData)
def get_zone_status(zone: str):
    conn = sqlite3.connect("aggregator.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, payload FROM sensor_data
        WHERE zone = ? ORDER BY timestamp DESC LIMIT 10
    """, (zone,))
    rows = cursor.fetchall()
    conn.close()

    data = {}
    for t, payload in rows:
        try:
            val = eval(payload)
            data[t] = val["value"]
        except:
            data[t] = payload
    return {"zone": zone, "readings": data}
