#!/usr/bin/python3
"""
main app for our flask app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
api_host = getenv("HBNB_API_HOST", "0.0.0.0")
api_port = getenv("HBNB_API_PORT", "5000")

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exc):
    """teardown the application"""
    storage.close()


if __name__ == "__main__":
    app.run(host=api_host, port=api_port, threaded=True)
