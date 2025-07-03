from fastapi import FastAPI
from routes import status, control, advice

app = FastAPI(title="Garden Monitoring API")

app.include_router(status.router, prefix="/status")
app.include_router(control.router, prefix="/control")
app.include_router(advice.router, prefix="/advice")
