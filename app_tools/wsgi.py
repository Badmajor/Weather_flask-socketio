import eventlet
from eventlet import wsgi
from app_tools import create_app

app = create_app()
wsgi.server(eventlet.listen(("127.0.0.1", 8000)), app)
