#!/usr/bin/env python3
"""the `filtered_logger` module
defines the function `filter_datum`
"""
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated from personal data"""
    for field in fields:
        message = re.sub(
            r"{}".format("{0}=([^{1}]+){1}".format(field, separator)),
            "{}={}{}".format(field, redaction, separator),
            message,
        )
    return message
