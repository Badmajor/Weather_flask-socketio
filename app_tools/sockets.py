from flask_socketio import emit, SocketIO

from .utils import record_data
from .weather_api import get_weather

socketio = SocketIO()


@socketio.on("weather")
def handler_weather(data: dict):
    response = get_weather(data.get("city"))
    location = response.get("location", None)
    user = data.get("user_session")
    if location:
        record_data(user, location)
    emit("response_weather", response)
