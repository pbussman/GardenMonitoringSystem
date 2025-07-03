from fastapi import APIRouter
from pydantic import BaseModel
from ml.decision_engine import get_irrigation_advice

router = APIRouter()

class AdviceRequest(BaseModel):
    zone: str

@router.post("/")
def generate_advice(req: AdviceRequest):
    # Stub example — eventually pull from DB
    recent_data = {"soil_moisture": 22, "temperature": 26}
    advice = get_irrigation_advice(req.zone, recent_data)
    return {"zone": req.zone, "recommendation": advice}
