#!/usr/bin/env python3
"""the auth.py module
defines the class `Auth`
"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """class for all authentication systems"""

    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """checks if auth is required for the given `path`"""
        if path is None:
            return True
        if not excluded_path or len(excluded_path) == 0:
            return True

        if path in excluded_path or (path + "/") in excluded_path:
            return False
        else:
            for ex_p in excluded_path:
                regex = ex_p[:ex_p.find("*")] + "." + ex_p[ex_p.find("*"):]
                if re.match(r"{}".format(regex), path):
                    return False
            return True

    def authorization_header(self, request=None) -> str:
        """returns authorization header's value if exists"""
        if request and request.headers.get('Authorization'):
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar("User"):
        """returns the current authorized user"""
        return None
