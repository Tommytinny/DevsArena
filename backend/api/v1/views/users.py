#!/usr/bin/python3
"""
Module of Users view
"""
from models import storage
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.app import auth
from api.v1.app import cache


@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
def all_users():
    """
    Retrieves the list of all State objects
    """
    
    key = "all_users"
    
    #check cache first
    cached_users = cache.get_cache(key)
    if cached_users:
        return jsonify(cached_users)
    
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    
    cache.set_cache(key, users_list)
    
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def retrieve_user(user_id):
    """ 
    fetch user data by user_id
    """
    if user_id is None:
        abort(404)

    if user_id == "me":
        if request.current_user is None:
            abort(404)
        else:
            return jsonify(request.current_user.to_dict())
        
    key = f"user:{user_id}"
    
    #check cache first
    cached_user = cache.get_cache(key)
    if cached_user:
        return jsonify(cached_user)
    
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    cache.set_cache(key, user.to_dict())
    
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        
    # Delete the user from the database
    user.delete()
    storage.save()
    
    # remove the user from the cache
    redis_keys = [f"user:{user_id}", "all_users"]
    for key in redis_keys:
        cache.delete_cache(key)
    
    return jsonify({}), 200


@app_views.route("/users", methods=['POST', 'OPTIONS'],
                 strict_slashes=False)
def create_user():
    """
    Creates a  new User Object and cache it
    """
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight OK'}), 200
    
    try:
        req = request.get_json()
    except Exception:
        return abort(400, {'message': 'Not a JSON'})

    if type(req) is not dict:
        return abort(400, {'message': 'Not a JSON'})
    
    # Check if email already exist in the database
    dictt = {} 
    dictt["email"] = request.form.get("email")
    user_exist = storage.search(User, dictt)
    if user_exist:
        return jsonify({"error": "Email address exist already"}), 404
    
    # Create the new user
    new_user = User(**req)
    new_user.save()
    
    # Cache the new user for 5 minutes
    cache.delete_cache("all_users")
    redis_key = f"user:{new_user.id}"
    cache.set_cache(redis_key, new_user.to_dict())
    
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object and cache the updated data.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        
    try:
        req = request.get_json()
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    check = ["id", "__class__", "created_at", "updated_at"]
    
    # Update user in the database
    for k, v in req.items():
        if k not in check:
            setattr(user, k, v)
    storage.save()
    
    # Update the cache for 5 minutes with the updated user
    cache.delete_cache("all_users")
    redis_key = f"user:{user_id}"
    cache.set_cache(redis_key, user.to_dict())
    
    return jsonify(user.to_dict()), 200
