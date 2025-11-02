#!/usr/bin/env python3
""" Session Authentication module
"""
from api.v1.auth.auth import Auth
import uuid
from models import storage
from models.user import User
from os import getenv
from flask import jsonify


class SessionAuth(Auth):
    """ Session Authentication Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session ID for a user id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return user ID based on session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        
        objs = self.user_id_by_session_id
        user_id = objs.get(session_id)
        return user_id
        """objs = storage.all(User)
        for value in objs.values():
            if value.session_id == session_id:
                return value.id"""

    def current_user(self, request=None) -> User:
        """ returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request)
        #print(request.headers)
        #print(session_id)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user_instance = storage.get(User, user_id)

        if user_instance is None:
            return None
        else:
            return user_instance

    def destroy_session(self, request=None) -> bool:
        """ deletes the user session / logout
        """
        if request is None:
            return False

        if self.session_cookie(request) is None:
            return False
        else:
            session_id = self.session_cookie(request)

        if self.user_id_for_session_id(session_id) is None:
            return False
        else:
            del self.user_id_by_session_id[session_id]
            return True
        
