#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Authentication Class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check request header for authentication requirement
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path and not path.endswith('/'):
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Getting Authorization value from request header
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """getting current user
        """
        return None

    def session_cookie(self, request=None) -> str:
        """ Return Cookie value from request
        """
        if request is None:
            return None

        return request.cookies.get(getenv("SESSION_NAME"))
