from flask import jsonify
from flask_restful import Resource

from ..database.models import City


class CityList(Resource):
    def get(self):
        cities = City.query.all()
        cities_list = [city.to_dict() for city in cities]
        return jsonify(cities_list)
