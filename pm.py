import bcrypt
from cryptography.fernet import Fernet
import base64
import sys
import re
import string
import random
import secrets
import hashlib
import pymysql
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
import chiavi

database_name = None



#connect, initialize and setup database

def generate_key(password, salt):
    password = password.encode()
    if isinstance(salt, str):
        salt = salt.encode()
    key = hashlib.pbkdf2_hmac('sha256', password, salt, 100000, dklen=32)  #100000 iterations, 32bytes = 256bit
    return base64.urlsafe_b64encode(key)

def initialize_db(db_name):
    global database_name

    config = {
        'host': chiavi.HOST,
        'user': chiavi.USER,
        'password': chiavi.PSW,
        'port': chiavi.PORT
    }

    database_name = db_name

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        except mysql.connector.Error as err:
            return 1
        
        cursor.close()
        conn.close()

        config['database'] = database_name
        conn = mysql.connector.connect(**config)
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Errore di autenticazione")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Il database non esiste")
        else:
            print(err)
        return 1

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
    
    if create_db() == 1:
        return 1
    return 0


def connect_existing_db(dbname):    #call this after login
    global database_name #sets database_name to be used to create connection
    database_name = dbname
    if create_db() == 1:
        return 1
    return 0

def create_connection():
    global database_name
    timeout = 15
    try: #this try except should be useless, is handled then
        connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db=database_name,
            host=chiavi.HOST,
            password=chiavi.PSW,
            read_timeout=timeout,
            port=chiavi.PORT,
            user=chiavi.USER,
            write_timeout=timeout,
        )
        return connection
    except pymysql.MySQLError as err:
        return None



def create_db():
    global database_name
    conn = create_connection()
    if conn == None:
        return 1
    try:
        with conn.cursor() as c:
            c.execute('''CREATE TABLE IF NOT EXISTS creditCard (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                name TEXT NOT NULL, 
                number BLOB NOT NULL, 
                expiryDate BLOB NOT NULL, 
                cvv TEXT, 
                salt BLOB NOT NULL, 
                UNIQUE KEY unique_number (number(255))
            )''')
        
            c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                service VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                encrypted_password BLOB NOT NULL, 
                note TEXT, 
                salt BLOB NOT NULL, 
                CONSTRAINT un1 UNIQUE (service, email)
            )''')
        
        conn.commit()

    finally:
        conn.close()




def create_users_db_connection():
    timeout = 15
    try:
        connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="Users",
            host=chiavi.HOST,
            password=chiavi.PSW,
            read_timeout=timeout,
            port=chiavi.PORT,
            user=chiavi.USER,
            write_timeout=timeout,
        )
        return connection
    except pymysql.MySQLError as err:
        return None


def create_users_table():

    conn = create_users_db_connection()
    if conn == None:
        return 1
    try:
        with conn.cursor() as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    db_name BLOB NOT NULL,
                    salt BLOB NOT NULL,
                    UNIQUE KEY unique_username (username)
                )
            ''')
        conn.commit()

    finally:
        conn.close()
        return 0

def generate_db_name(lenght=15):

  chars = string.ascii_letters + "_" #26*2+1 possible char, 53^15=7.3*10^25 different possible strings

  db_name = ''.join(random.choice(chars) for _ in range(lenght))

  return db_name

def add_user_to_users_table(username, master_password):

    db_name = generate_db_name()

    salt = bcrypt.gensalt()
    key = generate_key(master_password, salt)
    cipher_suite = Fernet(key)
    
    encrypted_db_name = cipher_suite.encrypt(db_name.encode())

    conn = create_users_db_connection()
    if conn == None:
        return 0, "error"
    try:
        with conn.cursor() as c:
            c.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
            result = c.fetchone()
            if result['COUNT(*)'] > 0:
                print(f"Errore: Username '{username}' già presente.")
                return 2, "error"

            c.execute('''
                INSERT INTO users (username, db_name, salt)
                VALUES (%s, %s, %s)
            ''', (username, encrypted_db_name, salt))
        
        conn.commit()
    except pymysql.IntegrityError as e:
        return 0, "error"
    finally:
        conn.close()

    return 1, db_name



def get_db_name(username, master_password):
    conn = create_users_db_connection()
    if conn == None:
        return "er"
    try:
        with conn.cursor() as c:
            c.execute('SELECT db_name, salt FROM users WHERE username = %s', (username,))
            result = c.fetchone()

            if result is None:
                print(f"Errore: Username '{username}' non trovato.")
                return None

            encrypted_db_name = result['db_name']
            salt = result['salt']

            key = generate_key(master_password, salt)
            cipher_suite = Fernet(key)

            try:
                decrypted_db_name = cipher_suite.decrypt(encrypted_db_name).decode()
                return decrypted_db_name
            except Exception as e:
                print(f"Errore: Impossibile decriptare il nome del database per lo username '{username}'. Master password errata.")
                return "mp"

    finally:
        conn.close()









#interact with database

def generate_password():
    while True:
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+{}:;<>,.?/~"
        
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%^&*()_+{}:;<>,.?/~")
        ]
        #12 char
        password += [secrets.choice(alphabet) for _ in range(14)]
        #shuffle order
        secrets.SystemRandom().shuffle(password)
        password = ''.join(password)
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}:;<>,.?/~])[A-Za-z\d!@#$%^&*()_+{}:;<>,.?/~]{10,}$'
        if re.match(pattern, password):
            return password

def add_password(service, email, password, note, master_password):
    try:
        salt = bcrypt.gensalt()
        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())

        conn = create_connection()
        c = conn.cursor()

        c.execute("INSERT INTO passwords (service, email, encrypted_password, note, salt) VALUES (%s, %s, %s, %s, %s)",
                  (service, email, encrypted_password, note, salt))
        conn.commit()
        # print("Password added successfully.")

    except pymysql.IntegrityError as e:
        # print(f"Error: Unable to add password. An entry with service '{service}' and email '{email}' already exists.")
        conn.close()
        return 0

    
    conn.close()
    return 1


def add_credit_card(name, number, expiry, cvv, master_password):
    conn = create_connection()
    c = conn.cursor()

    try:
        c.execute("SELECT number, salt FROM creditCard")
        existing_cards = c.fetchall()

        for el in existing_cards:
            enc_number = el['number']
            el_salt = el['salt']
            key = generate_key(master_password, el_salt)
            cipher_suite = Fernet(key)
            try:
                decrypted_card = cipher_suite.decrypt(enc_number).decode()
                if decrypted_card == number:
                    conn.close()
                    return 2
            except Exception as e:
                continue

        salt = bcrypt.gensalt()
        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)
        encrypted_number = cipher_suite.encrypt(number.encode())
        encrypted_expiry = cipher_suite.encrypt(expiry.encode())
        encrypted_cvv = cipher_suite.encrypt(cvv.encode())

        c.execute("INSERT INTO creditCard (name, number, expiryDate, cvv, salt) VALUES (%s, %s, %s, %s, %s)",
                  (name, encrypted_number, encrypted_expiry, encrypted_cvv, salt))
        conn.commit()

    except pymysql.IntegrityError as e:
        conn.close()
        return 0

    conn.close()
    return 1




def get_credit_Card(name, master_password):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT name, number, expiryDate, cvv, salt FROM creditCard WHERE name = %s", (name,))
            results = c.fetchall()

        if not results:
            print(f"No credit cards found for name '{name}'.")
            return None

        cards = []
        for result in results:
            encrypted_number = result['number']
            encrypted_expiry = result['expiryDate']
            encrypted_cvv = result['cvv']
            salt = result['salt']

            key = generate_key(master_password, salt)

            cipher_suite = Fernet(key)

            try:
                number = cipher_suite.decrypt(encrypted_number).decode()
                expiry = cipher_suite.decrypt(encrypted_expiry).decode()
                cvv = cipher_suite.decrypt(encrypted_cvv).decode()

                cards.append((name, number, expiry, cvv))
            except Exception as e:
                cards.append((name, '---', '---', '---'))
                # print(f"Error in decrypting card data for '{name}': {e}")
                continue

    finally:
        conn.close()

    return cards





def get_password(service, email, master_password):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT encrypted_password, salt FROM passwords WHERE service = %s AND email = %s", (service, email))
            result = c.fetchone()
    finally:
        conn.close()

    if result:
        encrypted_password = result['encrypted_password']
        salt = result['salt']
        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)
        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            return decrypted_password
        except Exception as e:
            # print(f"Error in decrypting: {e}")
            return None
    else:
        return None

def get_enc_psw(service, email):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT encrypted_password FROM passwords WHERE service = %s AND email = %s", (service, email))
            result = c.fetchone()
    finally:
        conn.close()

    if result:
        return result['encrypted_password']
    else:
        return None


    
def get_note(service, email):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT note FROM passwords WHERE service = %s AND email = %s", (service, email))
            result = c.fetchone()
    finally:
        conn.close()

    if result:
        return result['note']
    else:
        return ""

def get_mails(service):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT email FROM passwords WHERE service = %s", (service,))
            results = c.fetchall()
    finally:
        conn.close()

    return [result['email'] for result in results]



def del_credit_card(name, number, master_password):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT number, salt FROM creditCard WHERE name = %s", (name,))
            result = c.fetchone()
            
            if result:
                encrypted_number = result['number']
                salt = result['salt']
                
                key = generate_key(master_password, salt)
                cipher_suite = Fernet(key)
                
                try:
                    decrypted_number = cipher_suite.decrypt(encrypted_number).decode()
                    
                    if decrypted_number == number:
                        c.execute("DELETE FROM creditCard WHERE name = %s AND number = %s", (name, encrypted_number))
                        conn.commit()
                        return 1
                    else:
                        return 0
                except Exception as e:
                    return 0
            else:
                return 2
    finally:
        conn.close()



def remove_entry(service, email, master_password):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT encrypted_password, salt FROM passwords WHERE service = %s AND email = %s", (service, email))
            result = c.fetchone()

            if result:
                encrypted_password = result['encrypted_password']
                salt = result['salt']
                
                key = generate_key(master_password, salt)
                cipher_suite = Fernet(key)
                
                try:
                    cipher_suite.decrypt(encrypted_password).decode()
                    
                    c.execute("DELETE FROM passwords WHERE service = %s AND email = %s", (service, email))
                    conn.commit()
                    return 1
                except Exception as e:
                    print(f"Error in decrypting: {e}")
                    return 0
            else:
                return 2
    finally:
        conn.close()





def modify_entry(old_service, old_email, old_password, new_service, new_email, new_password, new_note, master_password):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT encrypted_password, salt FROM passwords WHERE service = %s AND email = %s", (old_service, old_email))
            result = c.fetchone()

            if result:
                encrypted_password = result['encrypted_password']
                salt = result['salt']

                key = generate_key(master_password, salt)
                cipher_suite = Fernet(key)

                try:
                    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
                    if old_password == decrypted_password:
                        c.execute("DELETE FROM passwords WHERE service = %s AND email = %s", (old_service, old_email))
                        conn.commit()
                        
                        add_password(new_service, new_email, new_password, new_note, master_password)
                        return 0
                    else:
                        print("Old password is wrong. Impossible to modify the entry.")
                        return 1
                except Exception as e:
                    print(f"Error in decrypting: {e}")
                    return 2
            else:
                print("No entry to modify found.")
                return 3
    finally:
        conn.close()


def print_all(master_password):
    conn = create_connection()
    c = conn.cursor()

    c.execute("SELECT service, email, encrypted_password, note, salt FROM passwords ORDER BY service")
    rows = c.fetchall()
    conn.close()

    if len(rows) == 0:
        print("Database is empty.\n")
        return [("---", "---", "---", "---")]

    list = []
    for row in rows:
        service = row['service']
        email = row['email']
        encrypted_password = row['encrypted_password']
        note = row.get('note', "")
        salt = row['salt']

        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)

        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            list.append((service, email, decrypted_password, note))
        except Exception as e:
            list.append((service, email, "---", "---"))
            print(f"Error decrypting for service '{service}' and email '{email}': {e}")
            continue

    return list


def delete_all(master_password):
    conn = None
    try:
        conn = create_connection()
        with conn.cursor() as c:
            c.execute("SELECT service, email, encrypted_password, salt FROM passwords")
            rows = c.fetchall()

            for row in rows:
                encrypted_password = row['encrypted_password']
                salt = row['salt']
                key = generate_key(master_password, salt)
                cipher_suite = Fernet(key)

                try:
                    cipher_suite.decrypt(encrypted_password).decode()
                except Exception:
                    if conn.open:
                        conn.close()
                    return 0

            c.execute("SELECT name, number, salt FROM creditCard")
            rows = c.fetchall()

            for row in rows:
                encrypted_number = row['number']
                salt = row['salt']
                key = generate_key(master_password, salt)
                cipher_suite = Fernet(key)

                try:
                    cipher_suite.decrypt(encrypted_number).decode()
                except Exception:
                    if conn.open:
                        conn.close()
                    return 0

            c.execute("DELETE FROM passwords")
            c.execute("DELETE FROM creditCard")
            
            conn.commit()
            return 1
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 0
    finally:
        if conn and conn.open:
            conn.close()


def find_by_mail(email, master_password):
    conn = create_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT service, email, encrypted_password, note, salt FROM passwords WHERE email = %s ORDER BY service", (email,))
            rows = c.fetchall()

            if not rows:
                print(f"Account '{email}' is not linked to any service.\n")
                return []
            
            result_list = []
            for row in rows:
                service = row['service']
                email = row['email']
                encrypted_password = row['encrypted_password']
                note = row['note']
                salt = row['salt']
                
                key = generate_key(master_password, salt)
                cipher_suite = Fernet(key)

                try:
                    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
                    result_list.append((service, email, decrypted_password, note))
                    # print(f"Email: '{email}', Service: '{service}', Password: '{decrypted_password}', Note: {note}")
                except Exception as e:
                    result_list.append((service, email, "---", "---"))
                    print(f"Error in decrypting for service '{service}' and email '{email}': {e}")
                    continue

            return result_list
    finally:
        conn.close()




def signal_handler(sig, frame):
    print("\n\nProgram closed by user.")
    sys.exit(0)

