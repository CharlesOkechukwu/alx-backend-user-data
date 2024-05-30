#!/usr/bin/env python3
"""module for a filtered logger datum"""
import logging
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns a redacted log message"""
    for field in fields:
        message = re.sub(fr'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message
