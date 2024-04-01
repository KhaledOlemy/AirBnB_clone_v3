#!/usr/bin/python3
"""Place class functions get/post/put/delete"""
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.user import User
from models import storage
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
import os


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


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def search_places():
    """return a single place on GET
       deletes a single place on DELETE
       updates a single place on PUT
    """
    all_places = storage.all(Place).values()
    if not request.get_json(force=True, silent=True):
        abort(400, description="Not a JSON")
    data = request.get_json(force=True, silent=True)
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    if not data or (not states and not cities and not amenities):
        return jsonify([place.to_dict() for place in all_places])
    city_ids = []
    if states:
        for state in states:
            city_ids += [city.id for city in storage.all(City).values() if city.state_id == state]
    if cities:
        for city in cities:
            if city not in city_ids:
                city_ids.append(city)
    if not city_ids:
        places = all_places
    else:
        places = []
        for place in all_places:
            if place.city_id in city_ids:
                places.append(place)
    
    # look here
    if not places:
        places = all_places
    # look here
    if not amenities:
        return jsonify([place.to_dict() for place in places])
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        amenities_as_objects = [storage.get(Amenity, a_id) for a_id in amenities]
        places = [place for place in places if all([amenity in place.amenities for amenity in amenities_as_objects])]
        qualified_places = []
        for place in places:
            place_dict = place.to_dict()
            place_dict.pop('amenities', None)
            places.append(place_dict)
        return jsonify(places)
    else:
        qualified_places = []
        for place in places:
            if all([a for a in amenities if a in place.amenity_ids]):
                qualified_places.append(place)
        return jsonify([place.to_dict() for place in qualified_places])


# @app_views.route("/places_search", methods=["POST"],
#                  strict_slashes=False)
# def search_places():
#     """return a single place on GET
#        deletes a single place on DELETE
#        updates a single place on PUT
#     """
#     all_places = storage.all(Place).values()
#     if not request.get_json(force=True, silent=True):
#         abort(400, description="Not a JSON")
#     data = request.get_json(force=True, silent=True)
#     if not data:
#         return jsonify([place.to_dict() for place in all_places])
#     cities = []
#     for item in data.get("states", []):
#         cities += [city.id for city in storage.all(City).values() if
#                    city.state_id == item]
#     for city in data.get("cities", []):
#         if city not in cities:
#             cities.append(city)
#     places = []
#     for item in cities:
#         places += [place for place in all_places if place.city_id == item]
#     if not places:
#         places = all_places
#     if not data.get('amenities'):
#         return jsonify([place.to_dict() for place in places])
#     desired_amenities = [storage.get(Amenity, amenity_id) for amenity_id
#                          in data.get('amenities')]
#     desired_places = [place for place in places if all([amenity in place.amenities
#                                                         for amenity in desired_amenities])]
#     return jsonify([place.to_dict() for place in desired_places])
