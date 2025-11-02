#!/usr/bin/python3
"""
Module of Resources View
"""
from models import storage
from models.project import Project
from models.resource  import Resource
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.app import cache

@app_views.route("/projects/<project_id>/resources", methods=['POST'],
                 strict_slashes=False)
def create_resource(project_id):
    """
    Creates a resource
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

    new_resource = Resource(**req)
    new_resource.save()
    
    # Cache the new task for 5 minutes
    cache.delete_cache("all_resources")

    return jsonify(new_resource.to_dict()), 201


@app_views.route("/projects/<project_id>/resources", methods=['GET'],
                 strict_slashes=False)
def resource_under_project(project_id):
    """
    Retrieves the list of all Resource objects under a Project
    """
    redis_key = "all_resources"
    
    # Check Redis cache first
    cached_resources = cache.get_cache(redis_key)
    if cached_resources:
        return jsonify(cached_resources)
    
    projects = storage.get(Project, project_id)
    if projects is None:
        abort(404)
        
    resources = storage.all(Resource).values()
    resource_list = [resource.to_dict() for resource in resources if resource.project_id == project_id]
    
    # Cache the list of resources in Redis for 5 minutes
    cache.set_cache(redis_key, resource_list)

    return jsonify(resource_list)


@app_views.route("/projects/<project_id>/resources/<recource_id>", methods=['GET'],
                 strict_slashes=False)
def retrieve_resource(project_id, resource_id):
    """
    Retrieves a Resource object
    """
    projects = storage.get(Project, project_id)
    if projects is None:
        abort(404)
    resource = storage.get(Resource, resource_id)
    if resource is None:
        abort(404)
    
    resources = storage.all(Resource).values()
    return jsonify(resources.to_dict())


@app_views.route("/projects/<project_id>/resources/<resource_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_resource(project_id, resource_id):
    """
    Deletes a Resource object
    """
    projects = storage.get(Project, project_id)
    if projects is None:
        abort(404)
    
    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404)
    resource.delete()
    storage.save()
    
    cache.delete_cache("all_resources")
    
    return jsonify({}), 200


@app_views.route("/projects/<project_id>/resources/<resource_id>", methods=['PUT'],
                 strict_slashes=False)
def update_resource(project_id, resource_id):
    """
    Updates a Resource object
    """
    projects = storage.get(Project, project_id)
    if projects is None:
        abort(404)
    
    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404)
    try:
        req = request.get_json()
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    check = ["id", "__class__", "project_id", "created_at", "updated_at"]

    for k, v in req.items():
        if k not in check:
            setattr(resource, k, v)
    storage.save()
    
    cache.delete_cache("all_resources")
    
    return jsonify(resource.to_dict()), 200
