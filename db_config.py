import os
from dotenv import load_dotenv

load_dotenv()

try:
    import mysql.connector
except ImportError:
    mysql = None

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE", "inventory")
}

# These definitions match the queries used by the application.
INVENTORY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stock INT NOT NULL,
    cp DECIMAL(12,2) NOT NULL,
    sp DECIMAL(12,2) NOT NULL,
    totalcp DECIMAL(14,2) NOT NULL,
    totalsp DECIMAL(14,2) NOT NULL,
    assumed_profit DECIMAL(14,2) NOT NULL,
    vendor VARCHAR(255),
    vendor_phoneno VARCHAR(50)
)
"""

USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def get_connection():
    """Create the inventory database/table if necessary, then return a connection."""
    if mysql is None:
        raise RuntimeError(
            "MySQL connector is not installed. Run: python -m pip install mysql-connector-python"
        )

    # First connect to MySQL without selecting a database. This fixes the
    # common case where the MySQL server exists but the inventory database
    # or its table has not yet been created.
    server_config = dict(DB_CONFIG)
    server_config.pop("database", None)

    server_con = None
    server_cursor = None
    try:
        server_con = mysql.connector.connect(**server_config)
        server_cursor = server_con.cursor()
        server_cursor.execute("CREATE DATABASE IF NOT EXISTS inventory")
        server_con.commit()
    finally:
        if server_cursor is not None:
            server_cursor.close()
        if server_con is not None and server_con.is_connected():
            server_con.close()

    con = mysql.connector.connect(**DB_CONFIG)
    cursor = con.cursor()
    try:
        cursor.execute(INVENTORY_TABLE_SQL)
        cursor.execute(USERS_TABLE_SQL)
        con.commit()
    finally:
        cursor.close()

    return con


def close_connection(connection, cursor=None):
    """Safely close a cursor and database connection."""
    try:
        if cursor is not None:
            cursor.close()
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
