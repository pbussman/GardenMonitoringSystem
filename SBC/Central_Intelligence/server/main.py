from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Route modules
from routes import status, control, advice

app = FastAPI(
    title="Garden Monitoring API",
    description="Backend for Smart Garden System (status, control, ML advice)",
    version="1.0.0"
)

# 🌐 Serve dashboard UI from /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🌱 Homepage shortcut
@app.get("/", include_in_schema=False)
def dashboard_home():
    return FileResponse("static/index.html")

# 🧪 Sensor + device status
app.include_router(status.router, prefix="/status", tags=["Status"])

# 🕹️ Relay + valve control
app.include_router(control.router, prefix="/control", tags=["Control"])

# 🧠 ML irrigation recommendation
app.include_router(advice.router, prefix="/advice", tags=["Advice"])
