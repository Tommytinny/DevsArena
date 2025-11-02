#!/usr/bin/python3
"""
index file
"""
from models import storage
from models.course import Course
from models.project import Project
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.caching.cache import Cache
from api.v1.app import cache


@app_views.route("/courses", methods=['GET'],
                 strict_slashes=False)
def list_all_courses():
    """
    Retrieves the list of all Course objects
    """
    key = "all_courses"
    
    #check cache first
    cached_courses = cache.get_cache(key)
    if cached_courses:
        return jsonify(cached_courses)
    
    courses = storage.all(Course).values()
    courses_list = [course.to_dict() for course in courses]
    
    cache.set_cache(key, courses_list)
    
    return jsonify(courses_list)



@app_views.route("/courses/<course_id>", methods=['GET'],
                 strict_slashes=False)
def retrieve_course(course_id):
    """
    Retrieves a Course object
    """
    key = f"course:{course_id}"
    
    #check cache first
    cached_course = cache.get_cache(key)
    if cached_course:
        return jsonify(cached_course)
    
    course = storage.get(Course, course_id)
    if course is None:
        abort(404)
    
    
    cache.set_cache(key, course.to_dict())
    
    return jsonify(course.to_dict())


@app_views.route("/courses/<course_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_course(course_id):
    """
    Deletes a Course object
    """
    course = storage.get(Course, course_id)
    if not course:
        abort(404)
    course.delete()
    storage.save()
    
    # remove the course from the cache
    redis_keys = [f"course:{course_id}", "all_courses"]
    for key in redis_keys:
        cache.delete_cache(key)
    
    return jsonify({}), 200


@app_views.route("/courses", methods=['POST'],
                 strict_slashes=False)
def create_course():
    """
    Creates a course
    """
    try:
        req = request.get_json()
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    if type(req) is not dict:
        return abort(400, {'message': 'Not a JSON'})

    """if 'name' not in req:
        return abort(400, {'message': 'Missing name'})"""

    new_course = Course(**req)
    new_course.save()
    
    # Cache the new course for 5 minutes
    cache.delete_cache("all_courses")
    redis_key = f"course:{new_course.id}"
    cache.set_cache(redis_key, new_course.to_dict())

    return jsonify(new_course.to_dict()), 201


@app_views.route("/courses/<course_id>", methods=['PUT'],
                 strict_slashes=False)
def update_course(course_id):
    """
    Updates a Course object
    """
    course = storage.get(Course, course_id)
    if not course:
        abort(404)
    try:
        req = request.get_json()
    except Exception as e:
        return abort(400, {'message': 'Not a JSON'})

    check = ["id", "__class__", "created_at", "updated_at"]

    for k, v in req.items():
        if k not in check:
            setattr(course, k, v)
    storage.save()
    
    # Update the cache for 5 minutes with the updated course
    cache.delete_cache("all_courses")
    redis_key = f"course:{course_id}"
    cache.set_cache(redis_key, course.to_dict())
    
    return jsonify(course.to_dict()), 200
