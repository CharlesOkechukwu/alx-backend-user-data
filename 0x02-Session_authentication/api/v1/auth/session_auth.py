#!/usr/bin/env python3
"""module for implementing session auth class"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from typing import TypeVar, Union


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

    def current_user(self, request=None) -> Union[TypeVar('User'), None]:
        """return a User instamce based on cookie value"""
        User.load_from_file()
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """destroy a session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
