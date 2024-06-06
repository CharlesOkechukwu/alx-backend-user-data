#!/usr/bin/env python3
"""module to implement auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class managing API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check path to confirm authentication requirement"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        for route in excluded_paths:
            if route.endswith('*') and path.startswith(route[:-1]):
                return False
            elif path == route or path + '/' == route:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """check the authorization header"""
        return None

    def current_user(self, request=None) -> str:
        """handle the current user"""
        return None
