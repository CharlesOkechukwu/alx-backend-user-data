#!/usr/bin/env python3
"""module to implement basic auth class"""
from .auth import Auth


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
