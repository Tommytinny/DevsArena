#!/usr/bin/python3
"""
index file
"""
from models import storage
from models.level import Level
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.app import cache


@app_views.route("/levels", methods=['GET'],
                 strict_slashes=False)
def list_all_levels():
    """
    Retrieves the list of all Level objects
    """
    redis_key = "all_levels"
    
    # Check Redis cache first
    cached_levels = cache.get_cache(redis_key)
    if cached_levels:
        return jsonify(cached_levels)
    
    # If not cached, fetch all levels from the database
    levels = storage.all(Level).values()
    levels_list = [level.to_dict() for level in levels]
    
    # Cache the list of levels in Redis for 5 minutes
    cache.set_cache(redis_key, levels_list)
    
    return jsonify(levels_list)


@app_views.route("/levels/<level_id>", methods=['GET'],
                 strict_slashes=False)
def retrieve_level(level_id):
    """
    Retrieves a Level object
    """
    redis_key = f"level:{level_id}"
    
    # Check Redis cache first
    cached_level = cache.get_cache(redis_key)
    if cached_level:
        return jsonify(cached_level)
    
    level = storage.get(Level, level_id)
    if level is None:
        abort(404)
    
    # Store level data in Redis (cache it) for future requests
    cache.set_cache(redis_key, level.to_dict())
    
    return jsonify(level.to_dict())


@app_views.route("/levels/<level_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_level(level_id):
    """
    Deletes a Level object
    """
    level = storage.get(Level, level_id)
    if not level:
        abort(404)
    level.delete()
    storage.save()
    
    # remove the level from the cache
    redis_keys = [f"level:{level_id}", "all_levels"]
    for key in redis_keys:
        cache.delete_cache(key)
    
    return jsonify({}), 200


@app_views.route("/levels", methods=['POST'],
                 strict_slashes=False)
def create_level():
    """
    Creates a level
    """
    try:
        req = request.get_json()
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    if type(req) is not dict:
        return abort(400, {'message': 'Not a JSON'})

    """if 'name' not in req:
        return abort(400, {'message': 'Missing name'})"""

    new_level = Level(**req)
    new_level.save()
    
    # Cache the new level for 5 minutes
    cache.delete_cache("all_levels")
    redis_key = f"level:{new_level.id}"
    cache.set_cache(redis_key, new_level.to_dict())

    return jsonify(new_level.to_dict()), 201


@app_views.route("/levels/<level_id>", methods=['PUT'],
                 strict_slashes=False)
def update_level(level_id):
    """
    Updates a Level object
    """
    level = storage.get(Level, level_id)
    if not level:
        abort(404)
    try:
        req = request.get_json()
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    check = ["id", "__class__",  "created_at", "updated_at"]

    for k, v in req.items():
        if k not in check:
            setattr(level, k, v)
    storage.save()
    
    # Update the cache for 5 minutes with the updated level
    cache.delete_cache("all_levels")
    redis_key = f"level:{level_id}"
    cache.set_cache(redis_key, level.to_dict())
    
    return jsonify(level.to_dict()), 200
