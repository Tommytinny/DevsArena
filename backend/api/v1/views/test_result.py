#!/usr/bin/python3
"""
Module of TestCases view
"""
from models import storage
from models.task  import Task
from models.test_result import TestResult
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/tasks/<task_id>/test_results", methods=['GET'],
                 strict_slashes=False)
def test_results_under_task(task_id):
    """
    Retrieves the list of all TestCase objects under a Task
    """
    tasks = storage.get(Task, task_id)
    if tasks is None:
        print("Task doesn't exist")
        abort(404, {"message": "Task doesn't exist"})
    
    test_results = storage.all(TestResult).values()
    test_result_list = [test_result.to_dict() for test_result in test_results if test_result.task_id == task_id]
    return jsonify(test_result_list)
