# Preparing and installing
You need to have a database that is running, either on your local machine, or online by using a service that lets you create a DB for free.
- **Aiven** is a web service where you can host a MySQL, postresql database for free (with some limitation of course): https://aiven.io/mysql.  
- **Docker** helps you create containers that are isolated from your computer; this allows you to run local application like webservers, databases, load-balancer...

> **_NOTE:_** depending on the type of database you are using, the statements can be quite different; you will need to adapt them to your need.

# Preparing the database
Beforehand, you need to create the architecture of your database. Here is how I would do that:

- User table with an ID, a username, and a master password.
- Password table with an ID, a userID that is the foreign key of the ID from the user table, and the hashed password.

The `init.sql` file can be found in the docker directory.

## Deployment with Docker
I will personally use Docker; if you wish to have an online database go on Aiven (or any other service that you like) and follow the documentation.
```bash
# Download the docker image mariadb:latest
docker pull mariadb

# Run the container
docker run --name pm-mariadb -v /home/lucas/projects/Password-Manager/docker/init.sql:/docker-entrypoint-initdb.d/init.sql -p 3306:3306 -e MARIADB_ROOT_PASSWORD=password -d mariadb
```
- **--name:** add a name to the container.
- **-v:** add a mount point between the local file init.sql to the entrypoint of the container; the script init.sql will be executed when the container runs for the first time, this will populate the database. The left part before **:** is the local path, and the right part the path inside the containers.
- **-p:** the ports that will be used to communicate between the host and the container.
- **-e:** environment variables, in that case the root password.
- **-d:** detach the container terminal.

```bash
# Access the MariaDB running container
docker exec -it pm-mariadb mariadb -uroot -p
```
- **-it:** interactive access to the container terminal.
- **-uroot:** use root user to connect.
- **-p:** give the password after.

The output of the exec command and some manipulations to verify the data inside the database can be found in the docker directory.

# Python implementation
## Package database
I create a package database to clean the project architecture a little bit; you can access any methods/functions in another file by using `from database.database import function_name`.
There are two different files:
- **simple_database.py:** similar to what I would do in a script, not in a project.
- **advanced_database.py:** a more advanced but better way of doing things; instead of letting a function handle the database connection, you can also create a class.

I added comment on my function to explain to you what is the logic behind them, event though they are simple; and you seem to understand pretty well what you are doing.
Using package are a good practice to have a clean project tree; the *__init__.py* file indicate to python that this is a package.
I returned boolean because you may want to test your functions, that way you know that it updated or not the data. For that you also need some exceptions handling that **_I did not_** do for sake of time.

# Summary
Before starting even coding, you should thing about the way you want to handle data and how your database should be architectured.
You also need to find the right database solution for your project, might be SQLite, but also MongoDB, postegresql or MariaDB; you need to figure this out.
SQLite is good for more project than people may think, but with user authentification I recommand you to lean in direction to MySQL, MariaDB etc. **_Make your own research, that is the most important!_**
Use packages to have a cleaner project.  
