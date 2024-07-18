import sqlite3
import bcrypt
from cryptography.fernet import Fernet
import base64
import sys
import signal
import getpass

# Funzione per generare una chiave di cifratura basata sulla MASTER PASSWORD
def generate_key(password, salt):
    password = password.encode()  # Converte la password in bytes
    key = bcrypt.kdf(password, salt, 32, 100)
    return base64.urlsafe_b64encode(key)

# Crea il database e la tabella se non esistono
def create_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, service TEXT, email TEXT, encrypted_password BLOB, note TEXT, salt BLOB)''')
    conn.commit()
    conn.close()

# Verifica se esiste già una password nel database con lo stesso service e email
def password_exists(service, email):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM passwords WHERE service = ? AND email = ?", (service, email))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

# Aggiungi una nuova password cifrata al database
def add_password(service, email, password, note, master_password):
    if password_exists(service, email):
        print(f"Esiste già l'account {email} per il servizio {service}.")
        return 0
    salt = bcrypt.gensalt()  # Genera un nuovo sale per ogni password
    key = generate_key(master_password, salt)
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("INSERT INTO passwords (service, email, encrypted_password, note, salt) VALUES (?, ?, ?, ?, ?)",
              (service, email, encrypted_password, note, salt))
    conn.commit()
    conn.close()
    print("PASSWORD AGGIUNTA")
    return 1


# Recupera e decifra una password dal database
def get_password(service, email, master_password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT encrypted_password, salt FROM passwords WHERE service = ? and email = ?", (service, email,))
    result = c.fetchone()
    conn.close()

    if result:
        encrypted_password, salt = result

        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)
        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            return decrypted_password
        except Exception as e:
            print(f"Errore nella decifratura: {e}")
            return None
    else:
        return None

def get_enc_psw(service, email):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT encrypted_password, salt FROM passwords WHERE service = ? and email = ?", (service, email,))
    result = c.fetchone()
    conn.close()
    print(result)
    return result[0]

def get_note(service, email):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT note FROM passwords WHERE service = ? and email = ?", (service, email,))
    result = c.fetchone()
    conn.close()
    return result if result else ""

# Recupera tutte le email associate a un service_name
def get_mails(service):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT email FROM passwords WHERE service = ?", (service,))
    results = c.fetchall()
    conn.close()
    return [result[0] for result in results]

# Rimuove un'entry dal database
def remove_entry(service, email, master_password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT encrypted_password, salt FROM passwords WHERE service = ? AND email = ?", (service, email))
    result = c.fetchone()
    
    if result:
        encrypted_password, salt = result
        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)
        
        try:
            cipher_suite.decrypt(encrypted_password).decode()
            c.execute("DELETE FROM passwords WHERE service = ? AND email = ?", (service, email))
            conn.commit()
            conn.close()
            print(f"Entry per il servizio {service} e l'email {email} rimossa.")
        except Exception as e:
            print(f"Errore nella decifratura: {e}")
    else:
        print("Nessuna entry da eliminare trovata corrispondente ai parametri specificati.")

def modify_entry(old_service, old_email, old_password, new_service, new_email, new_password, new_note, master_password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT encrypted_password, salt FROM passwords WHERE service = ? AND email = ?", (old_service, old_email))
    result = c.fetchone()

    if result:
        encrypted_password, salt = result
        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)

        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            if old_password == decrypted_password:
                c.execute("DELETE FROM passwords WHERE service = ? AND email = ?", (old_service, old_email))
                conn.commit()
                add_password(new_service, new_email, new_password, new_note, master_password)
                conn.close()
            else:
                print("Vecchia password non corretta. Impossibile modificare l'entry.")
        except Exception as e:
            print(f"Errore nella decifratura: {e}")
    else:
        print("Nessuna entry da modificare trovata corrispondente ai parametri specificati.")


def print_all(master_password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT service, email, encrypted_password, note, salt FROM passwords ORDER BY service")
    rows = c.fetchall()
    conn.close()
    if len(rows) == 0:
        print("Il database è vuoto.\n")
    for row in rows:
        service, email, encrypted_password, note, salt = row

        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)

        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            print(f"Servizio: {service}, Email: {email}, Password: {decrypted_password}, Note: {note}")
        except Exception as e:
            # Se la decrittazione fallisce, la master password è errata o c'è un errore nei dati
            print(f"Errore nella decifratura per il servizio {service} e l'email {email}.")
            continue    


def delete_all(master_password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT service, email, encrypted_password, salt FROM passwords")
    rows = c.fetchall()

    for row in rows:
        service, email, encrypted_password, salt = row
        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)

        try:
            # Prova a decrittare la password con la master password fornita
            cipher_suite.decrypt(encrypted_password).decode()
        except Exception as e:
            # Se fallisce la decifratura, significa che la master password è errata
            print("MASTER PASSWORD errata. Operazione annullata.")
            conn.close()
            return
    
    # Se tutte le decrittazioni hanno successo, elimina tutte le entry
    c.execute("DELETE FROM passwords")
    conn.commit()
    conn.close()
    print("Tutte le entry sono state eliminate.")


def find_by_mail(email, master_password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT service, email, encrypted_password, note, salt FROM passwords WHERE email = ? ORDER BY service", (email,))

    rows = c.fetchall()
    conn.close()
    if len(rows) == 0:
        print(f"L'account {email} non è collegato a nessun servizio.\n")
    for row in rows:
        service, email, encrypted_password, note, salt = row

        key = generate_key(master_password, salt)
        cipher_suite = Fernet(key)

        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            print(f"Email: {email}, Servizio: {service}, Password: {decrypted_password}, Note: {note}")
        except Exception as e:
            # Se la decrittazione fallisce, la master password è errata o c'è un errore nei dati
            print(f"Errore nella decifratura per il servizio {service} e l'email {email}.")
            continue    




def signal_handler(sig, frame):
    print("\n\nProgramma terminato dall'utente.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    create_db()
    print("---------------------------------------------------------")

    while True:
        print('\n')
        resp = input("Cosa vuoi fare?\n1- inserire nuove credenziali\n2- cercare una password già inserita\n3- modificare una password\n4- eliminare una password\n5- visualizzare l'intero database\n6- trovare tutti gli i servizi collegati a un account (mail o user)\n7- eliminare il database\ni- info\nQ- esci\n\n---------------------------------------------------------\n")
        print("---------------------------------------------------------")

        if resp.lower() == 'q':
            sys.exit(0)
        
        elif resp == '1':
            print("Inserimento nuova password")

            master_password = getpass.getpass(prompt="Inserisci la MASTER PASSWORD: ")
            master_password_confermation = getpass.getpass(prompt="Inserisci nuovamente la MASTER PASSWORD per conferma: ")


            while master_password_confermation != master_password:
                print("\nLe MASTER PASSWORD inserite non combaciano.")
                master_password = getpass.getpass(prompt="Inserisci la MASTER PASSWORD: ")
                master_password_confermation = getpass.getpass(prompt="Inserisci nuovamente la MASTER PASSWORD per conferma: ")


            service_name = input("Inserisci il nome del servizio: ")
            email = input("Inserisci la mail del nuovo account: ")
            password = input(f"Inserisci la password per l'account {email}: ")
            note = input("Inserisci eventuali note: ")

            add_password(service_name, email, password, note, master_password)
            print("---------------------------------------------------------")

        elif resp == '2':
            print("Cerca una password")

            master_password = getpass.getpass(prompt="Inserisci la MASTER PASSWORD: ")
            service_name = input("Inserisci il nome del servizio per recuperare la password: ")
            mails = get_mails(service_name)

            if not mails:
                print("Servizio non trovato.")

            elif len(mails) == 1:
                retrieved_mail = mails[0]
                retrieved_password = get_password(service_name, retrieved_mail, master_password)
                retrieved_note = get_note(service_name, retrieved_mail)[0]

                if retrieved_password:
                    print(f"La password per l'account {retrieved_mail} di {service_name} è: {retrieved_password}")
                    if retrieved_note == "":
                        print("Non ci sono note")
                    else:
                        print(f"Le note per {service_name} sono: {retrieved_note}")
                    print("---------------------------------------------------------")
                else:
                    print("MASTER PASSWORD errata o errore nella decifratura.")
            else:
                print(f"Esistono più account per il servizio {service_name}.")
                print("Scegli quello per cui recuperare la password:")
                for index, mail in enumerate(mails, start=1):
                    print(f"{index}. {mail}")

                try:
                    choice = int(input("Inserisci il numero corrispondente: "))
                    if 1 <= choice <= len(mails):
                        retrieved_mail = mails[choice - 1]
                        retrieved_password = get_password(service_name, retrieved_mail, master_password)
                        retrieved_note = get_note(service_name, retrieved_mail)[0]

                        if retrieved_password:
                            print(f"La password per l'account {retrieved_mail} di {service_name} è: {retrieved_password}")
                            if retrieved_note == "":
                                print("Non ci sono note")
                            else:
                                print(f"Le note per {service_name} sono: {retrieved_note}")
                            print("---------------------------------------------------------")
                        else:
                            print("MASTER PASSWORD errata o errore nella decifratura.")
                    else:
                        print("Scelta non valida.")
                except ValueError:
                    print("Scelta non valida. Devi inserire un numero.")

        elif resp == '3':
            print("Modifica di una password")
            master_password = getpass.getpass(prompt="Inserisci la MASTER PASSWORD: ")

            old_service = input("Inserisci il servizio da modificare: ")
            old_email = input("Inserisci il vecchio account da modificare: ")
            old_password = input("Inserisci la vecchia password da modificare: ")
            old_note = get_note(old_service, old_email)[0]

            print()
            new_service = input("Inserisci il nuovo servizio: ")
            new_email = input("Inserisci il nuovo account: ")
            new_password = input(f"Inserisci la nuova password per l'account {new_email}: ")
            new_note = input("Inserisci le nuove note: ") or old_note

            modify_entry(old_service, old_email, old_password, new_service, new_email, new_password, new_note, master_password)
            print("---------------------------------------------------------")

        elif resp == '4':
            print("Eliminazione di una password")
            master_password = getpass.getpass(prompt="Inserisci la MASTER PASSWORD: ")

            service_name = input("Inserisci il nome del servizio: ")
            email = input("Inserisci la mail dell'account da eliminare: ")
            password = input(f"Inserisci la password dell'account {email} per confermare: ")
            safety = input(f"Sei sicuro di voler eliminare la password dell'account {email}? Premi Y per continuare, qualsiasi altro tasto per annullare: ")
            if safety.lower() == 'y':
                if get_password(service_name, email, master_password) == password:
                    remove_entry(service_name, email, master_password)
                else:
                    print("Password errata. Impossibile eliminare l'entry.")
            print("---------------------------------------------------------")


        elif resp == '5':
            print("Visualizza tutto il database")
            master_password = getpass.getpass(prompt="Inserisci la MASTER PASSWORD: ")
            print_all(master_password)
            print("---------------------------------------------------------")  

        elif resp == '6':
            print("Visualizza tutti i servizi collegati allo stesso account")
            mail = input("Inserisci account da cercare: ")
            master_password = getpass.getpass(prompt="Inserisci la MASTER PASSWORD: ")
            find_by_mail(mail, master_password)
            



        elif resp == '7':
            print("Elimina tutto il database")

            master_password = getpass.getpass(prompt="Inserisci la MASTER PASSWORD: ")

            print("ATTENZIONE! Questa operazione è IRREVERSIBILE. I dati andranno persi.")
            safety = input("Sei sicuro di voler eliminare l'intero database? Premi Y per continuare, qualsiasi altro tasto per annullare: ")
            if safety.lower() == 'y':
                delete_all(master_password)

        elif resp.lower() == 'i':
            print("Scegli il servizio desiderato inserendo il numero corrispondente.")
            print("ATTENZIONE: devi utilizzare la stessa MASTER PASSWORD sia per l'inserimento che per la ricerca di una password, altrimenti non sarà possibile erogare il servizio!")
            print("Dovrai ricordarti a memoria la MASTER PASSWORD, la quale non potrà essere inserita nel database.")
            print("Nel campo email puoi inserire sia il classico indirizzo di posta elettronica usato per quell'account oppure Nome Utente o UserID.")
            print("Puoi modificare il servizio, la mail, la password e/o le note di ogni entry. L'operazione SOVRASCRIVE i vecchi dati.")
            print("Puoi eliminare una entry confermandone servizio, mail e password perdendo DEFINITIVAMENTE le rispettive informazioni.")
            print("---------------------------------------------------------\n")

        else:
            print("Inserisci un input valido tra 1, 2, 3, 4 o Q.")
