#!/usr/bin/env python3
"""the `basic_auth` module.
defines the class `BasicAuth`
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


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

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """returns the extracted username and password
        from `decoded_base64_authorization_header`"""
        if (
            decoded_base64_authorization_header
            and type(decoded_base64_authorization_header) is str
        ):
            if decoded_base64_authorization_header.find(":") != -1:
                user_data = decoded_base64_authorization_header.split(":")
                return (user_data[0], user_data[1])

        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str):
        """returns a `User` instance based on `user_email`, `user_pwd`"""
        if user_email and type(user_email) is str:
            if user_pwd and type(user_pwd) is str:

                User.load_from_file()  # load data from file
                if User.count() > 0:  # User objects exists
                    user = User.search({"email": user_email})
                    if user:
                        user = User(**(user[0].to_json(True)))
                        if user.is_valid_password(user_pwd):
                            return user

    def current_user(self, request=None) -> TypeVar("User"):
        """returns the current user"""
        auth_header = self.authorization_header(request)
        encoded = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(
            encoded
        )
        username_pass = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(
            username_pass[0], username_pass[1]
        )
        return user
