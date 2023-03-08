#!/usr/bin/env python3
"""the `session_exp_auth` module
defines the class `SessionExpAuth`
"""
from datetime import datetime
from datetime import timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """adds expiration and storage on top of Session Authentication"""

    def __init__(self) -> None:
        duration = os.getenv("SESSION_DURATION")
        self.session_duration = int(duration) if duration else 0

    def create_session(self, user_id: str = None) -> str:
        session_id = super().create_session(user_id)
        if session_id:
            session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        if session_id and session_id in self.user_id_by_session_id.keys():
            if "created_at" in self.user_id_by_session_id[session_id].keys():
                first = self.user_id_by_session_id[session_id]["created_at"]
                second = timedelta(seconds=self.session_duration)
                if self.session_duration <= 0:
                    return self.user_id_by_session_id[session_id]["user_id"]
                elif first + second > datetime.now():
                    return self.user_id_by_session_id[session_id]["user_id"]
