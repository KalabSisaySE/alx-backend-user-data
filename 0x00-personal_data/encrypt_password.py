#!/usr/bin/env python3
"""the encrypt_password module
defines the functions `hash_password` and `is_valid`
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns the hashed version `password`"""
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
