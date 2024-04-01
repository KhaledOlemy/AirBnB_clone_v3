#!/usr/bin/python3
"""Place class functions get/post/put/delete"""
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"],
                 strict_slashes=False)
def get_all_places(city_id):
    """return all places for GET and creates new place on POST"""
    linked_city = [city for city in
                   storage.all(City).values() if city.id == city_id]
    if not linked_city:
        abort(404)
    if request.method == "GET":
        all_instances = [place.to_dict() for place in
                         storage.all(Place).values() if
                         place.city_id == city_id]
        return jsonify(all_instances)
    elif request.method == "POST":
        if not request.get_json(force=True, silent=True):
            abort(400, description="Not a JSON")
        data = request.get_json(force=True, silent=True)
        if 'user_id' not in data:
            abort(400, description="Missing user_id")
        linked_user = [user for user in storage.all(User).values()
                       if user.id == data['user_id']]
        if not linked_user:
            abort(404)
        if 'name' not in data:
            abort(400, description="Missing name")
        data['city_id'] = city_id
        new_instance = Place(**data)
        new_instance.save()
        return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_single_place(place_id):
    """return a single place on GET
       deletes a single place on DELETE
       updates a single place on PUT
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not request.get_json(force=True, silent=True):
            abort(400, description="Not a JSON")
        data = request.get_json(force=True, silent=True)
        for key, value in data.items():
            if key not in ["id", "user_id", "city_id",
                           "created_at", "updated_at"]:
                setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
