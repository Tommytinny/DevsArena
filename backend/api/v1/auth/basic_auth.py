#!/usr/bin/env python3
""" Basic Auth module
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """ Basic authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracting base64 authorization header
        """
        if authorization_header is None:
            return None
        else:
            if not isinstance(authorization_header, str):
                return None
            if not authorization_header.startswith("Basic "):
                return None
            else:
                base64_header = authorization_header.split(" ")
                return base64_header[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """ decode base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        else:
            if not isinstance(base64_authorization_header, str):
                return None
            try:
                encode_header = base64_authorization_header.encode('utf-8')
                decode_header = base64.b64decode(encode_header)
                decoded_header = decode_header.decode('utf-8')
            except BaseException:
                return None

            return decoded_header

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):
        """ Extracting user credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None
        else:
            if not isinstance(decoded_base64_authorization_header, str):
                return None, None
            if decoded_base64_authorization_header.find(':') == -1:
                return None, None
            else:
                v = decoded_base64_authorization_header.split(':', 1)
                return v[0], v[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user_exist = User.search({'email': user_email})
        except Exception:
            return None

        for user in user_exist:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request
        """
        auth_h = self.authorization_header(request)
        if auth_h is None:
            return None

        ext_auth_h = self.extract_base64_authorization_header(auth_h)
        if ext_auth_h is None:
            return None

        d_auth_h = self.decode_base64_authorization_header(ext_auth_h)
        if d_auth_h is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(d_auth_h)
        if user_email is None and user_pwd is None:
            return None

        user_credentials = self.user_object_from_credentials(
            user_email, user_pwd)
        if user_credentials is None:
            return
        else:
            return user_credentials
