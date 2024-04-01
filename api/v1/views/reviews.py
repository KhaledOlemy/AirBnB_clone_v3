#!/usr/bin/python3
"""Review class functions get/post/put/delete"""
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """return all reviews for GET and creates new review on POST"""
    linked_place = [place for place in
                    storage.all(Place).values() if place.id == place_id]
    if not linked_place:
        abort(404)
    if request.method == "GET":
        all_instances = [review.to_dict() for review in
                         storage.all(Review).values() if
                         review.place_id == place_id]
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
        if 'text' not in data:
            abort(400, description="Missing text")
        data['place_id'] = place_id
        new_instance = Review(**data)
        new_instance.save()
        return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_single_review(review_id):
    """return a single review on GET
       deletes a single review on DELETE
       updates a single review on PUT
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not request.get_json(force=True, silent=True):
            abort(400, description="Not a JSON")
        data = request.get_json(force=True, silent=True)
        for key, value in data.items():
            if key not in ["id", "user_id", "place_id",
                           "created_at", "updated_at"]:
                setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
