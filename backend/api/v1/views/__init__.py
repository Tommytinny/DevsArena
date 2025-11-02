#!/usr/bin/python3
"""
initializing blueprint
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

@app_views.after_request
def after_request(response) -> None:
    
    header = response.headers
    header['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    header['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    header['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    header['Access-Control-Allow-Credentials'] = 'true'
    
    return response

from api.v1.views.auth import *
from api.v1.views.index import *
from api.v1.views.levels import *
from api.v1.views.users import *
from api.v1.views.courses import *
from api.v1.views.projects import *
from api.v1.views.resources import *
from api.v1.views.tasks import *
from api.v1.views.test_cases import *
from api.v1.views.session_auth import *
from api.v1.views.submission import *
from api.v1.views.test_result import *
from api.v1.views.events import *
from api.v1.views.timetables import *
