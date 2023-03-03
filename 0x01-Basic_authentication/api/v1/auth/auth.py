#!/usr/bin/env python3
"""the auth.py module
defines the class `Auth`
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class for all authentication systems"""

    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """checks if auth is required"""
        if path is None:
            return True
        if not excluded_path or len(excluded_path) == 0:
            return True
        if path in excluded_path or (path + "/") in excluded_path:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """returns authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """returns the current authorized user"""
        return None
