from database.advanced_database import open_connection_db, close_connection_db
from pm import generate_password

# Global variables
connection = open_connection_db("root", "password", "127.0.0.1", "password_manager", 3306)

# Create the password
# For example purpose, I did not hash the password; there is just the logic of making a DB connection
def create_password_db(userid: int) -> bool:
    password = generate_password()
    statement = "INSERT INTO password (userID, hashed_password) VALUES (?, ?)"
    connection.cursor().execute(statement, (userid, password))
    connection.commit()
    close_connection_db(connection)
    return True

# Update a given password (id) by a new password (password)
def update_password_db(id:int, password:str) -> bool:
    statement = "UPDATE password SET password = (?) WHERE id = (?)"
    connection.cursor().execute(statement, (password, id))
    connection.commit()
    close_connection_db(connection)
    return True

# Delete the password using the ID
def delete_password_db(id) -> bool:
    statement = "DELETE FROM password WHERE id = (?)"
    connection.cursor().execute(statement, (id))
    connection.commit()
    close_connection_db(connection)
