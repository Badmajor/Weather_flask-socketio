import uuid

from flask import Blueprint, jsonify, render_template, request, session
from sqlalchemy import desc

from .database import db, models
from .database.utils import get_or_create
from .database.models import User, UsersCities
from .weather_api import get_cities

index_bp = Blueprint("index", __name__)
get_city_suggestions_bp = Blueprint("suggestions", __name__)
api_bp = Blueprint("api", __name__)


@index_bp.route("/")
def index():
    city_history = request.args.get("c", "")
    if not (user_session := session.get("user_session", None)):
        user_session = str(uuid.uuid4())
        session["user_session"] = user_session
        user = models.User(user_session=user_session)
        db.session.add(user)
        db.session.commit()
    else:
        user, _ = get_or_create(User, user_session=user_session)
    user_cities = (
        UsersCities.query.filter_by(user_id=user.id)
        .order_by(desc(UsersCities.created_at))
        .limit(10)
        .all()
    )
    requests_history = [uc.city.name for uc in user_cities]
    return render_template(
        "index.html",
        user_session=user_session,
        requests_history=requests_history,
        city_history=city_history,
    )


@get_city_suggestions_bp.route("/get_city_suggestions")
def get_city_suggestions():
    query = request.args.get("q", "")
    suggestions = []
    if len(query) > 2:
        suggestions = get_cities(query)
    return jsonify(suggestions)
