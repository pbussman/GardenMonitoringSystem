def get_irrigation_advice(zone, recent_readings):
    moisture = recent_readings.get("soil_moisture", 100)
    if moisture < 30:
        return {"action": "water", "duration_min": 12}
    else:
        return {"action": "skip"}

