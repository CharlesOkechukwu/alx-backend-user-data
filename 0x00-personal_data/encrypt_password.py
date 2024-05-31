#!/usr/bin/env python3
"""module to handle encrypting and validating passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """takes string password and returned hashed passowrd"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """compare if passowrd is a valid passowrd"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
