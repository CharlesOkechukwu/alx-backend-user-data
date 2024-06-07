#!/usr/bin/env python3
"""module to implement db storage auth class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from typing import TypeVar, Union


class SessionDBAuth(SessionExpAuth):
    """manage db stroage session authentication"""
    def create_session(self, user_id: str = None) -> str:
        """create a session id for user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = super().create_session(user_id)
        if session_id is not None:
            user = UserSession(user_id=user_id, session_id=session_id)
            user.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return user_id from session_id"""
        if session_id is None:
            return None
        users_list = UserSession.search({'session_id': session_id})
        if users_list != []:
            user = users_list[0]
            duration = timedelta(seconds=self.session_duration)
            if user.created_at + duration < datetime.now():
                return None
            return user.user_id
        return None

    def destroy_session(self, request=None) -> bool:
        """destroy a session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        users_list = UserSession.search({'session_id': session_id})
        if users_list != []:
            users_list[0].remove()
            return True
        return False
