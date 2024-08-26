--- If you have any questions about mariadb you can check some references here: https://mariadb.com/kb/en/sql-statements/
-- Create the database
CREATE DATABASE IF NOT EXISTS password_manager;

-- Use the database in which the tables will be created
USE password_manager;

-- Create the tables needed
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    master VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS password (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    FOREIGN KEY(userID) REFERENCES users(id)
);

-- Insert example data
INSERT INTO users (username, master) VALUES
    ('Pietro', 'thatisalongpassword'),
    ('Lucas', 'supermastersecretpassword'),
    ('Cherry', 'longestpasswordofthelistbecauseilikesecurity');

INSERT INTO password(userID, hashed_password) VALUES
    (1, 'password01'),
    (1, 'password02'),
    (1, 'password03'),
    (1, 'password04'),
    (2, 'wordpass01'),
    (2, 'wordpass02'),
    (2, 'wordpass03'),
    (3, 'yot01'),
    (3, 'yot02'),
    (3, 'yot03'),
    (3, 'yot04');
