#!/usr/bin/python3
"""State class functions get/post/put/delete"""
from models.user import User
from models import storage
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def get_all_users():
    """return all users for GET and creates new user on POST"""
    if request.method == "GET":
        all_instances = [user.to_dict() for user in
                         storage.all(User).values()]
        return jsonify(all_instances)
    elif request.method == "POST":
        if not request.get_json(force=True, silent=True):
            abort(400, description="Not a JSON")
        data = request.get_json(force=True, silent=True)
        if 'name' not in data:
            abort(400, description="Missing name")
        new_instance = User(**data)
        new_instance.save()
        return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_single_user(user_id):
    """return a single user on GET
       deletes a single user on DELETE
       updates a single user on PUT
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not request.get_json(force=True, silent=True):
            abort(400, description="Not a JSON")
        data = request.get_json(force=True, silent=True)
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
