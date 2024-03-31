#!/usr/bin/python3
"""
INDEX page of our flask blueprints
"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models import storage

@app_views.route("/status")
def status_function():
    """simple status json to return"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats_function():
    """returns count for each class"""
    classes = [Amenity, City, State, User, Place, Review]
    out_dict = {}
    for classname in classes:
        out_dict[classname.__tablename__] = storage.count(classname)
    return jsonify(out_dict)
