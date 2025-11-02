#!/usr/bin/env python3
""" Module of auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask_cors import cross_origin
from models.user import User
from os import getenv
from api.v1.app import auth
from models import storage


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def auth_login():
    """ POST /api/v1/login
            - starting a session
    """
    if request.form.get("email") == "" or not request.form.get("email"):
        return jsonify({"error": "email missing"}), 400

    if request.form.get("password") == "" or not request.form.get("password"):
        return jsonify({"error": "password missing"}), 400

    dictt = {}
    dictt["email"] = request.form.get("email")

    user_exist = storage.search(User, dictt)

    if not user_exist:
        return jsonify({"error": "no user found for this email"}), 404

    for user in user_exist:
        if not user.is_valid_password(request.form.get("password")):
            return jsonify({"error": "wrong password"}), 401
        else:
            access_token = auth.create_token(request.form.get("email"))
            return jsonify({"access_token": access_token}), 200
