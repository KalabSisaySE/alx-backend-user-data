#!/usr/bin/env python3
"""the `session_db_auth` module
a user session that can be saved in the database
defines the class SessionDBAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """manages a session that can be stored in a database"""

    def create_session(self, user_id: str = None) -> str:
        """creates and stores a new session for a `user_id`"""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(
                **{"user_id": user_id, "session_id": session_id}
            )
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user_id for a session_id from database
        if session is not expired"""
        if session_id in self.user_id_by_session_id.keys():
            if "created_at" in self.user_id_by_session_id[session_id].keys():
                first = self.user_id_by_session_id[session_id]["created_at"]
                second = timedelta(seconds=self.session_duration)
                # check if session has not expired first
                if first + second > datetime.now():
                    sessions = UserSession.search({"session_id": session_id})
                    # if session is found
                    if len(sessions) > 0:
                        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """deletes the current session from database and memory"""
        if request and self.session_cookie(request):
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id=session_id)
            # if there is a user is found for the given session_id
            if user_id:
                user_session = UserSession.get(session_id)
                user_session.remove()
                del self.user_id_by_session_id[session_id]
                return True
        return False
