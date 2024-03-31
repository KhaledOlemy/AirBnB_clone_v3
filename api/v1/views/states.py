from models.state import State
from models import storage
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def get_all_states():
    """return all states"""
    if request.method == "GET":
        all_instances = [state.to_dict() for state in
                         storage.all(State).values()]
        return jsonify(all_instances)
    elif request.method == "POST":
        if not request.get_json():
            abort(400, description="Not a JSON")
        data = request.get_json()
        if 'name' not in data:
            abort(400, description="Missing name")
        new_instance = State(**data)
        new_instance.save()
        return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_single_state(state_id):
    """return a single state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    elif request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not request.get_json():
            abort(400, description="Not a JSON")
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
