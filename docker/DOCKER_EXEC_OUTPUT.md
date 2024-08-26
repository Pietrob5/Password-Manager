```bash
(\wsl.localhost\Ubuntulucasome0ucas\projects\Password-Manager5.1env) lucas@lucas:~/projects/Password-Manager$ docker exec -it pm-mariadb mariadb -uroot -p
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 4
Server version: 11.5.2-MariaDB-ubu2404 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| password_manager   |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.001 sec)

MariaDB [(none)]> use password_manager;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [password_manager]> show tables;
+----------------------------+
| Tables_in_password_manager |
+----------------------------+
| password                   |
| users                      |
+----------------------------+
2 rows in set (0.000 sec)

MariaDB [password_manager]> select * from users;
+----+----------+----------------------------------------------+
| id | username | master                                       |
+----+----------+----------------------------------------------+
|  1 | Pietro   | thatisalongpassword                          |
|  2 | Lucas    | supermastersecretpassword                    |
|  3 | Cherry   | longestpasswordofthelistbecauseilikesecurity |
+----+----------+----------------------------------------------+
3 rows in set (0.004 sec)
```