#!/usr/bin/env python3
"""the `filtered_logger` module
defines the function `filter_datum`
"""
import logging
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """instantiates a new `RedactingFormatter` object"""
        self.fields = list(fields)
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """formats the record according to the specified format"""
        msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        record.msg = msg.replace(";", "; ")[:-1]
        return logging.Formatter(self.FORMAT).format(record=record)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(RedactingFormatter())
    logger.addHandler(sh)
    logger.propagate = False
    return logger
