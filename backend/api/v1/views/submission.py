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
from models.submission import Submission
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.app import app
from werkzeug.utils import secure_filename
import os
import subprocess
from api.v1.app import cache


app.config['UPLOAD_FOLDER'] = './uploads'
app.config['TEST_FOLDER'] = './tests'
app.config['ALLOWED_EXTENSIONS'] = {'py', 'c', 'cpp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app_views.route("/submissions", methods=['POST'],
                 strict_slashes=False)
def create_submission():
    """
    Creates a submission
    """
    from api.v1.app import auth
    user = auth.current_user(request)
    if user is None:
        abort(404)
    # Support two modes: file upload (multipart/form) and inline code (JSON)
    request_data = {}
    # Inline JSON with code
    if request.is_json:
        try:
            req = request.get_json()
        except Exception:
            return abort(400, {'message': 'Not a JSON'})

        code = req.get('code')
        language = req.get('language')
        project_id = req.get('project_id')
        task_id = req.get('task_id')
        if not code or not language:
            return abort(400, {'message': 'Missing code or language'})

        # choose extension
        ext = 'py' if language.lower().startswith('py') else ('c' if language.lower().startswith('c') and '++' not in language else 'cpp')
        # create upload paths
        import uuid
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], user.id)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        filename = f"submission_{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(user_dir, filename)
        # save code to file
        with open(filepath, 'w') as f:
            f.write(code)

        request_data = {
            'file_url': filepath,
            'student_id': user.id,
            'language': language,
            'project_id': project_id,
            'task_id': task_id
        }
    else:
        # multipart/form upload
        file = None
        if 'file' in request.files:
            file = request.files['file']
        language = request.form.get('language')
        if file:
            if file.filename == '':
                abort(400, {'message': 'No file selected'})

            extension = file.filename.rsplit('.', 1)[1].lower()
            if '.' not in file.filename and extension not in {'py', 'c', 'cpp'}:
                abort(400, {'message': 'Invalid file type'})

            if language == 'Python' and extension != 'py':
                abort(400, {'message': 'Not a Python file type'})

            if language == 'C' and extension != 'c':
                abort(400, {'message': 'Not a C file type'})

            if language == 'C++' and extension != 'cpp':
                abort(400, {'message': 'Not a C++ file type'})

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file_name = os.path.join(user.id, filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                if os.path.exists(filepath):
                    return abort(400, {'message': 'File already exist'})

                file.save(filepath)
                request_data = request.form.to_dict()
                request_data['file_url'] = filepath
                request_data['student_id'] = user.id

    new_submission = Submission(**request_data)
    new_submission.save()

    return jsonify(new_submission.to_dict()), 201


@app_views.route("/projects/<project_id>/submissions", methods=['GET'],
                 strict_slashes=False)
def all_submission(project_id):
    """
    Retrieves the list of all Submission objects
    """
    
    from api.v1.app import auth
    user = auth.current_user(request)
    if user is None:
        abort(404)
    
    projects = storage.get(Project, project_id)
    if projects is None:
        abort(404)
        
    submissions = storage.all(Submission).values()
    submission_list = [submission.to_dict() for submission in submissions if submission.project_id == project_id and submission.student_id == user.id]
    
    
    return jsonify(submission_list)


@app_views.route("/projects/<project_id>/tasks/<task_id>/submissions", methods=['GET'],
                 strict_slashes=False)
def retrieve_submission(project_id, task_id):
    """
    Retrieves a Submission object
    """
    
    from api.v1.app import auth
    user = auth.current_user(request)
    if user is None:
        abort(404)
    
    
    project = storage.get(Project, project_id)
    if project is None:
        abort(404)
    
    task = storage.get(Task, task_id)
    if task is None:
        abort(404)
    
    submissions = storage.all(Submission).values()
    submission = [submission.to_dict() for submission in submissions if submission.task_id == task_id and submission.project_id == project_id and submission.student_id == user.id]
    
    
    return jsonify(submission)



@app_views.route("/submissions/<submission_id>", methods=['PUT'],
                 strict_slashes=False)
def update_submission(submission_id):
    """
    Updates a submission object
    """
    submission = storage.get(Submission, submission_id)
    if submission is None:
        abort(404)
    from api.v1.app import auth
    user = auth.current_user(request)
    file = request.files['file']
    language = request.form['language']
    if file:
        if file.filename == '':
            return abort(400, {'message': 'No file selected'})
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        if '.' not in file.filename and extension not in {'py', 'c', 'cpp'}:
            return abort(400, {'message': 'Invalid file type'})
        
        if language == 'Python' and extension != 'py':
            return abort(400, {'message': 'Not a Python file type'})
        
        if language == 'C' and extension != 'c':
            return abort(400, {'message': 'Not a C file type'})
        
        if language == 'C++' and extension != 'cpp':
            return abort(400, {'message': 'Not a C++ file type'})
        
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            file_name = os.path.join(user.id, filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            if os.path.exists(filepath):
                os.remove(filepath)
            
            file.save(filepath)
            request_data = request.form.to_dict()
            request_data['file_url'] = filepath
            request_data['student_id'] = user.id
            
    check = ["id", "__class__", "created_at", "updated_at"]
    for k, v in request_data.items():
        if k not in check:
            setattr(submission, k, v)
    storage.save()
    
    test_results = storage.all(TestResult).values()
    for test_result in test_results:
        if test_result.submission_id == submission.id:
            test_result.delete()
    storage.save()

    #for k, v in req.items():
        #if k not in check:
            #setattr(submission, k, v)
    #storage.save()SW
    
    return jsonify(submission.to_dict()), 200



@app_views.route("/tasks/<task_id>/submissions/<submission_id>", methods=['POST'],
                 strict_slashes=False)
def submission_checker(task_id, submission_id):
    """
    Task code checker
    """
    # Enqueue grading job and return immediately. Grading is performed by a background worker.
    try:
        req = request.get_json()
    except Exception:
        return abort(400, {'message': 'Not a JSON'})

    if type(req) is not dict:
        return abort(400, {'message': 'Not a JSON'})

    from api.v1.app import auth
    user = auth.current_user(request)
    if user is None:
        abort(404, {"message": "No current session"})

    project = storage.get(Project, req.get('project_id'))
    if project is None:
        abort(404, {"message": "Project doesn't exist"})

    submission = storage.get(Submission, submission_id)
    if submission is None:
        abort(404, {"message": "Submission doesn't exist"})

    task = storage.get(Task, task_id)
    if task is None:
        abort(404, {"message": "Task doesn't exist"})

    # Enqueue job using RQ (Redis Queue)
    try:
        import redis as _redis
        from rq import Queue
        from api.v1.tasks.grader import process_submission

        redis_conn = _redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        q = Queue('grading', connection=redis_conn)
        job = q.enqueue(process_submission, submission_id, task_id, req.get('project_id'), user.id, req.get('language'), submission.file_url)
        return jsonify({'job_id': job.get_id(), 'status': 'queued'}), 202
    except Exception as e:
        # If queueing fails, return server error (worker may not be available)
        print("Failed to enqueue grading job:", str(e))
        return abort(500, {"message": "Failed to enqueue grading job"})


@app_views.route('/jobs/<job_id>', methods=['GET'], strict_slashes=False)
def job_status(job_id):
    """Return RQ job status and result metadata."""
    try:
        import redis as _redis
        from rq.job import Job
        redis_conn = _redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        job = Job.fetch(job_id, connection=redis_conn)
        data = {
            'id': job.get_id(),
            'status': job.get_status(),
            'result': job.result,
            'exc_info': str(job.exc_info) if job.exc_info else None
        }
        return jsonify(data), 200
    except Exception as e:
        return abort(404, {'message': 'job not found'})
