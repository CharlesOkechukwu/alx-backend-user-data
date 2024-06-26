#!/usr/bin/env python3
"""module to implement basic auth class"""
from .auth import Auth
import base64
from typing import Tuple, TypeVar, Union
from api.v1.views.users import User


class BasicAuth(Auth):
    """class to manage API basic authentication"""
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """extract base64 authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> Tuple[str]:
        """extract and return user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(':')
        return credentials[0], ':'.join(credentials[1:])

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> Union[TypeVar('User'), None]:
        """return user instance from db file using credentials"""
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        User.load_from_file()
        if User.count() == 0:
            return None
        users = User.search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """check current user and overload Auth"""
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(base64_header)
        email, pwd = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(email, pwd)
