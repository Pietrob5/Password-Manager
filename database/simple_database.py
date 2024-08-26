# This package is a simple implementation to connects to the database.
# You may need to adapt the credentials to your need.
# This resource will help you adapt what you have already implemented: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

import mariadb

conn = mariadb.connect(
        user="root",
        password="password",
        host="127.0.0.1",
        port=3306,
        database="password_manager"
)

cur = conn.cursor()

# retrieving information
cur.execute("SELECT id,username FROM users")

for id, username in cur:
    print(f"id: {id}, username: {username}")

conn.close()