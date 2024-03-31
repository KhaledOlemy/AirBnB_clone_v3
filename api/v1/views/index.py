from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status")
def status_function():
    return jsonify({"status": "OK"})
