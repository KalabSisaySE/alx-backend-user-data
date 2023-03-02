#!/usr/bin/env python3
"""the `filtered_logger` module
defines the function `filter_datum`
"""
import logging
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a mysql connection object"""
    return mysql.connector.connect(
        host=os.getenv(key="PERSONAL_DATA_DB_HOST", default="localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv(key="PERSONAL_DATA_DB_USERNAME", default="root"),
        password=os.getenv(key="PERSONAL_DATA_DB_PASSWORD", default=""),
    )


def main():
    """retrieve users data from the database
    and lists them in a formatted way"""
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    records = cursor.fetchall()
    users = []
    for record in records:
        user = ""
        for attr, value in zip(cursor.description, record):
            user = user + "{}={};".format(attr[0], value)
        users.append(user)

    for user in users:
        record = logging.LogRecord(
            "my_db", logging.INFO, None, None, user, None, None
        )
        formatter = RedactingFormatter(PII_FIELDS)
        print(formatter.format(record))


if __name__ == "__main__":
    main()
