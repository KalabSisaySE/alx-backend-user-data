#!/usr/bin/env python3
"""the `auth` module
defines the function `_hash_password`
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Union
from uuid import uuid4
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """takes in a `password` string arguments and returns bytes"""
    password = bytes(password, "utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """hashes the password and registers a user
        if email does not alread exists"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pass = _hash_password(password)
            user = self._db.add_user(email, hashed_pass)
            return user

    def valid_login(self, email, password):
        """verifies if a user exists/already registered"""
        try:
            user = self._db.find_user_by(email=email)
            hashed_pass = user.hashed_password
        except NoResultFound:
            hashed_pass = None
        return bcrypt.checkpw(hashed_pass, password)

    def create_session(self, email: str) -> str:
        """generates a session for a user and returns it"""
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            pass
        finally:
            return session_id

    def valid_login(self, email: str, password: str) -> bool:
        """checks if the given `password` is correct"""
        given_pass = bytes(password, "utf-8")
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(given_pass, user.hashed_password)
        except (NoResultFound, InvalidRequestError):
            return False

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """returns the user based on the given `session_id`"""
        if session_id:
            try:
                return self._db.find_user_by(session_id=session_id)
            except (NoResultFound, InvalidRequestError):
                return

    def destroy_session(self, user_id: int):
        """destroies the session id that is stored under the `user_id`"""
        if user_id:
            try:
                self._db.update_user(user_id, session_id=None)
            except (NoResultFound, InvalidRequestError):
                return

    def get_reset_password_token(self, email: str) -> str:
        """generates a new reset token, saves it and returns it"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """updates the password based on the `reset_token`"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pass = _hash_password(password)
            self._db.update_user(
                user.id, password=hashed_pass, reset_token=None
            )
        except (NoResultFound, InvalidRequestError):
            raise ValueError
