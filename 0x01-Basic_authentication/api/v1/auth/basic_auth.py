#!/usr/bin/env python3
"""the `basic_auth` module.
defines the class `BasicAuth`
"""
import base64
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

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """decodes the Base64 string and returns it"""
        if base64_authorization_header and \
           type(base64_authorization_header) is str:
            try:
                decode_binary = base64.b64decode(
                    bytes(base64_authorization_header, "utf-8")
                )
                return decode_binary.decode("utf-8")
            except Exception:
                return
