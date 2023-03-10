#!/usr/bin/env python3
"""the `user_session` module
defines the class `UserSession`
"""
from models.base import Base


class UserSession(Base):
    """a models for a user_session to store in the database"""

    def __init__(self, *args: list, **kwargs: dict):
        """instantiates a new `UserSession` object"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
