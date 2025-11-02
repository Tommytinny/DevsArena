#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask_cors import cross_origin
from models.user import User
from os import getenv
from api.v1.app import auth
from models import storage


@app_views.route('auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """ POST /api/v1/auth_session/login
            - starting a session
    """
    email = request.get_json()['email']
    password = request.get_json()['password']
    if email == "" or not email:
        return jsonify({"error": "Email missing"}), 400

    if password == "" or not password:
        print("password missing")
        return jsonify({"error": "Password missing"}), 400

    dictt = {}
    dictt["email"] = email

    user_exist = storage.search(User, dictt)

    if not user_exist:
        return jsonify({"error": "No user found with this email address"}), 404

    for user in user_exist:
        if not user.is_valid_password(password):
            return jsonify({"error": "Wrong password"}), 404
        else:
            access_token = auth.create_token(email)
            return jsonify({"access_token": access_token}), 200


@app_views.route('auth_session/logout',
                 methods=['GET'], strict_slashes=False)
@cross_origin()
def auth_session_logout():
    """ DELETE /api/v1/auth_session/logout
            - delete user session
    """
    destroy_session = auth.destroy_session(request)
    if not destroy_session:
        abort(404)
    else:
        response = jsonify({})
        response.delete_cookie(getenv("SESSION_NAME"))
        return response
  

@app_views.route('auth_session', methods=['GET'], strict_slashes=False)
@cross_origin()
def auth_session():
    """ GET /api/v1/auth_session
            - verify session
    """
    user = auth.current_user(request)

    if user is None:
        return jsonify({}), 401
    else:
        return jsonify({}), 200
