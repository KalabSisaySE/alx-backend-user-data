#!/usr/bin/env python3
"""the `auth` module
defines the function `_hash_password`
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes in a `password` string arguments and returns bytes"""
    password = bytes(password, "utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt())
