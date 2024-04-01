#!/usr/bin/python3
"""Amenity class functions get/post/put/delete"""
from models.amenity import Amenity
from models import storage
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def get_all_amenities():
    """return all amenities for GET and creates new amenity on POST"""
    if request.method == "GET":
        all_instances = [amenity.to_dict() for amenity in
                         storage.all(Amenity).values()]
        return jsonify(all_instances)
    elif request.method == "POST":
        if not request.get_json():
            abort(400, description="Not a JSON")
        data = request.get_json()
        if 'name' not in data:
            abort(400, description="Missing name")
        new_instance = Amenity(**data)
        new_instance.save()
        return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_single_amenity(amenity_id):
    """return a single amenity on GET
       deletes a single amenity on DELETE
       updates a single amenity on PUT
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not request.get_json():
            abort(400, description="Not a JSON")
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
