#!/usr/bin/python3
"""
INDEX page of our flask blueprints
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status_function():
    """simple status json to return"""
    return jsonify({"status": "OK"})
