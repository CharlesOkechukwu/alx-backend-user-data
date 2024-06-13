#!/usr/bin/env python3
"""module for authentication and password hashing"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hashes the string password and return hashed bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
