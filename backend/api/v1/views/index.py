#!/usr/bin/python3
"""
Module of index view
"""
from models import storage
from models.user import User
from models.course import Course
from models.project import Project
from models.resource import Resource
from models.task import Task
from models.test_case import TestCase
from models.event import Event
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """
    Return a JSON response with status OK
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """
    endpoint that retrieves the number of each objects by type
    """
    return jsonify({
        "users": storage.count(User),
        "courses": storage.count(Course),
        "projects": storage.count(Project),
        "tasks": storage.count(Task),
        "test_cases": storage.count(TestCase),
        "events": storage.count(Event),
        })

@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized_error() -> None:
    """ GET /api/v1/unauthorized
    Response:
      - raise a 401 error
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden_error() -> None:
    """ GET /api/v1/forbidden
    Response:
      - raise a 403 error
    """
    abort(403)
