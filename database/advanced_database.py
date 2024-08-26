# This package is a more advanced way of connecting to the database.
# You may need to adapt the credentials to your need.
# This resource will help you adapt what you have already implemented: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

import mariadb

from pm import generate_password

def open_connection_db(user, password, host, database: str, port: int) -> mariadb.connections.Connection:
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    return conn

def close_connection_db(connection:mariadb.connections.Connection) -> bool:
    connection.close()
    return True
