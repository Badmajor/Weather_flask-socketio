from app_tools import app, config, socketio

if __name__ == "__main__":
    socketio.run(app, debug=config.DEBUG)
