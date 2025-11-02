#!/usr/bin/python3
"""
Module of Tasks view
"""
from models import storage
from models.user import User
from models.project import Project
from models.task  import Task
from models.test_case import TestCase
from models.test_result import TestResult
from api.v1.auth.session_auth import SessionAuth
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.app import cache


@app_views.route("/projects/<project_id>/tasks", methods=['POST'],
                 strict_slashes=False)
def create_task(project_id):
    """
    Creates a task
    """
    project = storage.get(Project, project_id)
    if project is None:
        abort(404)
    try:
        req = request.get_json()  
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    if type(req) is not dict:
        return abort(400, {'message': 'Not a JSON'})
    
    req['project_id'] = project_id
    """if 'name' not in req:
        return abort(400, {'message': 'Missing name'})"""

    new_task = Task(**req)
    new_task.save()
    

    return jsonify(new_task.to_dict()), 201


@app_views.route("/projects/<project_id>/tasks", methods=['GET'],
                 strict_slashes=False)
def tasks_under_project(project_id):
    """
    Retrieves the list of all Task objects under a Project
    """

    
    projects = storage.get(Project, project_id)
    if projects is None:
        abort(404)
        
    tasks = storage.all(Task).values()
    task_list = [task.to_dict() for task in tasks if task.project_id == project_id]
    

    return jsonify(task_list)


@app_views.route("/projects/<project_id>/tasks/<task_id>", methods=['GET'],
                 strict_slashes=False)
def retrieve_task(project_id, task_id):
    """
    Retrieves a Task object
    """
    
    project = storage.get(Project, project_id)
    if project is None:
        abort(404, {"message": "Project doesn't exist"})
        
    task = storage.get(Task, task_id)
    if task is None:
        abort(404, {"message": "Task doesn't exist"})
    
    return jsonify(task.to_dict())


@app_views.route("/tasks/<task_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_task(task_id):
    """
    Deletes a Task object
    """
    task = storage.get(Task, task_id)
    if not task:
        abort(404)
    task.delete()
    storage.save()
    
    return jsonify({}), 200


@app_views.route("/projects/<project_id>/tasks/<task_id>", methods=['PUT'],
                 strict_slashes=False)
def update_task(task_id):
    """
    Updates a task object
    """
    task = storage.get(Task, task_id)
    if not task:
        abort(404)
    try:
        req = request.get_json()
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    check = ["id", "__class__", "project_id", "created_at", "updated_at"]

    for k, v in req.items():
        if k not in check:
            setattr(task, k, v)
    storage.save()
    
    
    return jsonify(task.to_dict()), 200
