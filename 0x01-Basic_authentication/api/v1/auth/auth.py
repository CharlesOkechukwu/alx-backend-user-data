#!/usr/bin/env python3
"""module to implement auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class managing API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check path to confirm authentication requirement"""
        return False

    def authorization_header(self, request=None) -> str:
        """check the authorization header"""
        return None

    def current_user(self, request=None) -> str:
        """handle the current user"""
        return None
