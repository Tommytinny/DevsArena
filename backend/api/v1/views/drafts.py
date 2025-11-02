#!/usr/bin/python3
"""Drafts view module

Endpoints to save and retrieve inline editor drafts per user and task.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.draft import Draft


@app_views.route('/tasks/<task_id>/drafts', methods=['GET'], strict_slashes=False)
def get_draft(task_id):
    from api.v1.app import auth
    user = auth.current_user(request)
    if user is None:
        abort(404)

    drafts = storage.all(Draft).values()
    for d in drafts:
        if getattr(d, 'task_id', None) == task_id and getattr(d, 'user_id', None) == user.id:
            return jsonify(d.to_dict())

    return jsonify({}), 200


@app_views.route('/tasks/<task_id>/drafts', methods=['POST'], strict_slashes=False)
def save_draft(task_id):
    try:
        req = request.get_json()
    except Exception:
        return abort(400, {'message': 'Not a JSON'})

    from api.v1.app import auth
    user = auth.current_user(request)
    if user is None:
        abort(404)

    code = req.get('code')
    language = req.get('language')
    if code is None:
        return abort(400, {'message': 'Missing code'})

    # find existing draft
    drafts = storage.all(Draft).values()
    existing = None
    for d in drafts:
        if getattr(d, 'task_id', None) == task_id and getattr(d, 'user_id', None) == user.id:
            existing = d
            break

    if existing:
        existing.code = code
        existing.language = language
        storage.save()
        return jsonify(existing.to_dict()), 200

    new_draft = Draft(user_id=user.id, task_id=task_id, code=code, language=language)
    new_draft.save()
    return jsonify(new_draft.to_dict()), 201
