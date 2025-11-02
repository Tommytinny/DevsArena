#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.jwt_auth import JWTAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.caching.cache import Cache


app = Flask(__name__)
CORS(app, resources={
    r"/api/v1/*": {
        "origins": ["http://localhost:5173"],
        "supports_credentials": True
    }
})

app.register_blueprint(app_views)


cache = Cache()
auth = getenv("AUTH_TYPE", None)
jwt_secret_key = getenv("SECRET_KEY", None)

if auth:
    if auth == 'basic_auth':
        auth = BasicAuth()
    elif auth == 'session_auth':
        auth = SessionAuth()
    elif auth == 'auth':
        auth = Auth()
    elif auth == 'JWT':
        auth = JWTAuth(app=app, secret_key=jwt_secret_key, token_expires_in_minutes=60)


@app.before_request
def request_handler() -> None:
    """ Authentication request handler
    Return:
        - None if auth is None
    """
    if auth is None:
        pass
    else:
        if not auth.require_auth(request.path,
                                 ['/api/v1/status/', '/api/v1/unauthorized/',
                                  '/api/v1/forbidden/',
                                  '/api/v1/auth_session/login/', '/api/v1/auth_session/']):
            pass
        else:
            if not isinstance(auth, SessionAuth):
                if request.method == 'OPTIONS':
                    return jsonify({"message": "successful"}), 200
                if auth.authorization_header(request) is None:
                    abort(401)
            if auth.current_user(request) is None:
                abort(403)
            else:
                if auth.authorization_header(
                   request) and auth.session_cookie(request):
                    return None, abort(401)
                
                request.current_user = auth.current_user(request)

@app.errorhandler(400)
def bad_request(error) -> str:
    """ Bad request handler
    """
    error_message = error.description.get('message') if error.description.get('message') else "Bad request"
    return jsonify({'error': error_message}), 400

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    #error_message = error.description.get('message') if error.description.get('message') else "Not found"
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


        
if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True, debug=True)
