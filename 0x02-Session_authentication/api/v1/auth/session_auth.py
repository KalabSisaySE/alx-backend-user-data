#!/usr/bin/env python3
"""the session_auth module
implements a session authentication
"""
from flask import request
from uuid import uuid4
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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

    def current_user(self, request=None) -> TypeVar("User"):
        """returns a user based on the session_id on the request's cookie"""
        auth = Auth()
        session_id = auth.session_cookie(request=request)
        user_id = self.user_id_for_session_id(session_id=session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """deletes the current session of a logged user"""
        if request and self.session_cookie(request):
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id=session_id)
            if user_id:
                del self.user_id_by_session_id[session_id]
                return True
        return False
