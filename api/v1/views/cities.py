#!/usr/bin/python3
"""City class functions get/post/put/delete"""
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def get_all_cities(state_id):
    """return all cities for GET and creates new city on POST"""
    linked_state = [state for state in
                    storage.all(State).values() if state.id == state_id]
    if not linked_state:
        abort(404)
    if request.method == "GET":
        all_instances = [city.to_dict() for city in
                         storage.all(City).values() if
                         city.state_id == state_id]
        return jsonify(all_instances)
    elif request.method == "POST":
        if not request.get_json(force=True, silent=True):
            abort(400, description="Not a JSON")
        data = request.get_json(force=True, silent=True)
        if 'name' not in data:
            abort(400, description="Missing name")
        data['state_id'] = state_id
        new_instance = City(**data)
        new_instance.save()
        return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_single_city(city_id):
    """return a single city on GET
       deletes a single city on DELETE
       updates a single city on PUT
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not request.get_json(force=True, silent=True):
            abort(400, description="Not a JSON")
        data = request.get_json(force=True, silent=True)
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
