from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_session.redis import RedisSessionInterface
from redis import Redis

from . import config
from .api.resourses import CityList
from .database import db
from .sockets import socketio


def create_app():
    flask_app = Flask(__name__)

    flask_app.config["SECRET_KEY"] = config.SECRET_KEY
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = (
        config.SQLALCHEMY_DATABASE_URI
    )
    flask_app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
    flask_app.session_interface = RedisSessionInterface(
        app=flask_app,
        client=Redis(host=config.REDIS_HOST, port=config.REDIS_PORT),
    )
    api = Api(flask_app)
    api.add_resource(CityList, "/api/v1/cities")

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    from .routers import index_bp, get_city_suggestions_bp

    flask_app.register_blueprint(index_bp)
    flask_app.register_blueprint(get_city_suggestions_bp)

    socketio.init_app(flask_app)

    return flask_app


app = create_app()
