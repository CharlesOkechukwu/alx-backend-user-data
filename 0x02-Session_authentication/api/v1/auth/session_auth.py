#!/usr/bin/env python3
"""module for implementing session auth class"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """class to manage API session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create a session id for user-id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """extract user-id for session id"""
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id, None)