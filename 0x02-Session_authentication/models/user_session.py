#!/usr/bin/env python3
"""module to implement db user storage class"""
from models.base import Base
from datetime import datetime


class UserSession(Base):
    """implement User Session storage class"""
    def __init__(self, *args: list, **kwargs: dict):
        """initialize User Session instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.created_at = datetime.now()
