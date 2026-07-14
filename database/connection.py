"""
============================================================
OTT STREAM INTELLIGENCE PLATFORM
Database Connection Manager
============================================================
"""

import mysql.connector
from mysql.connector import Error

from config import *


def get_connection():
    """
    Returns a MySQL connection.
    """

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():

            return connection

    except Error as e:

        print(f"MySQL Connection Error : {e}")

        raise