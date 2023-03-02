#!/usr/bin/env python3
"""the encrypt_password module
defines the functions `hash_password` and `is_valid`
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns the hashed version `password`"""
    return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """verifies that password matches the hashed one `hashed_password`"""
    return bcrypt.checkpw(bytes(password, "utf-8"), hashed_password)
