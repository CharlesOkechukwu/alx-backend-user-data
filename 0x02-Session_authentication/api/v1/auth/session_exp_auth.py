#!/usr/bin/env python3
"""module to implement session expiry auth class"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from typing import TypeVar, Union


class SessionExpAuth(SessionAuth):
    """class to manage session id expiration"""
    def __init__(self) -> None:
        """initialize session expiration instance"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """create a session id for user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return user_id from session_id"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            return None
        created_at = session_dict.get('created_at')
        duration = timedelta(seconds=self.session_duration)
        if created_at + duration < datetime.now():
            return None
        return session_dict.get('user_id')
