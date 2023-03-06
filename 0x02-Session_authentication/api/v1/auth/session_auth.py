#!/usr/bin/env python3
"""the session_auth module
implements a session authentication
"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """session authentication class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user id and returns the session id"""
        if user_id and type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrieves the user's id for a given `session_id`"""
        if session_id and type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
