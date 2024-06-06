#!/usr/bin/env python3
"""module to implement basic auth class"""
from .auth import Auth
import base64
from typing import Tuple


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
