from fastapi import APIRouter
from pydantic import BaseModel
import paho.mqtt.publish as publish

router = APIRouter()

class Command(BaseModel):
    node: str
    channel: str
    state: str  # "on" or "off"

@router.post("/relay")
def send_command(cmd: Command):
    topic = f"garden/command/{cmd.node}/relay"
    payload = {"channel": cmd.channel, "state": cmd.state}
    publish.single(
        topic, payload=str(payload),
        hostname="192.168.1.100",
        auth={'username': 'garden', 'password': 'growgreen'}
    )
    return {"status": "sent", "topic": topic}
