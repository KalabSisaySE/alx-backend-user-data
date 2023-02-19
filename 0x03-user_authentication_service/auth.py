#!/usr/bin/env python3
"""the `auth` module
defines the function `_hash_password`
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """takes in a `password` string arguments and returns bytes"""
    password = bytes(password, "utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt())


def _generate_uuid():
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

    def create_session(email):
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
