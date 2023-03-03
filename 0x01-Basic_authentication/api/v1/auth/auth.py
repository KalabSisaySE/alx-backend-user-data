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
        return False

    def authorization_header(self, request=None) -> str:
        """returns authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """returns the current authorized user"""
        return None
