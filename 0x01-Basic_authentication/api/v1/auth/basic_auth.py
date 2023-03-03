#!/usr/bin/env python3
"""the `basic_auth` module.
defines the class `BasicAuth`
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """returns the Base64 part of the `Authorization` header"""
        if authorization_header and type(authorization_header) is str:
            if authorization_header.startswith("Basic "):
                idx = authorization_header.find(" ") + 1
                return authorization_header[idx:]

    pass
