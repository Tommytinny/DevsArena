#!/usr/bin/python3
"""
Module of TestCases view
"""
from models import storage
from models.task  import Task
from models.test_case import TestCase
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/tasks/<task_id>/test_cases", methods=['POST'],
                 strict_slashes=False)
def create_test_case(task_id):
    """
    Creates a test_case
    """
    task = storage.get(Task, task_id)
    if task is None:
        abort(401)
    try:
        req = request.get_json()  
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    if type(req) is not dict:
        return abort(400, {'message': 'Not a JSON'})
    
    req['task_id'] = task_id
    """if 'name' not in req:
        return abort(400, {'message': 'Missing name'})"""

    new_test_case = TestCase(**req)
    new_test_case.save()

    return jsonify(new_test_case.to_dict()), 201


@app_views.route("/tasks/<task_id>/test_cases", methods=['GET'],
                 strict_slashes=False)
def test_cases_under_task(task_id):
    """
    Retrieves the list of all TestCase objects under a Task
    """
    tasks = storage.get(Task, task_id)
    if tasks is None:
        abort(404)
        
    test_cases = storage.all(TestCase).values()
    test_case_list = [test_case.to_dict() for test_case in test_cases if test_case.task_id == task_id]
    return jsonify(test_case_list)


@app_views.route("/test_cases/<test_case_id>", methods=['GET'],
                 strict_slashes=False)
def retrieve_test_case(test_case_id):
    """
    Retrieves a TestCase object
    """
    test_case = storage.get(TestCase, test_case_id)
    if test_case is None:
        abort(404)
    
    test_cases = storage.all(TestCase).values()
    return jsonify(test_cases.to_dict())


@app_views.route("/test_cases/<test_case_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_test_case(test_case_id):
    """
    Deletes a TestCase object
    """
    test_case = storage.get(TestCase, test_case_id)
    if not test_case:
        abort(404)
    
    test_case.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/test_cases/<test_case_id>", methods=['PUT'],
                 strict_slashes=False)
def update_test_case(test_case_id):
    """
    Updates a TestCase object
    """
    test_case = storage.get(TestCase, test_case_id)
    if not test_case:
        abort(404)
    try:
        req = request.get_json()
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    check = ["id", "__class__", "task_id", "created_at", "updated_at"]

    for k, v in req.items():
        if k not in check:
            setattr(test_case, k, v)
    storage.save()
    return jsonify(test_case.to_dict()), 200
