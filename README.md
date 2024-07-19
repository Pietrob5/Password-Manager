# Password Manager

This project is a password manager application written in Python. It allows users to securely store, retrieve, modify, and delete passwords associated with various services and accounts. The passwords are encrypted using the `cryptography.fernet` module, which utilizes AES encryption. The master password is used to generate encryption keys and is never stored in the database.

## Features

- **Add Passwords**: Store new passwords securely in the database.
- **Retrieve Passwords**: Retrieve passwords for specified services and accounts.
- **Modify Passwords**: Update existing passwords and associated details.
- **Delete Passwords**: Remove specific passwords from the database.
- **View All Entries**: Display all stored passwords.
- **Find Services by Email**: List all services associated with a particular email.
- **Delete All Entries**: Remove all entries from the database.

## Prerequisites

- Python 3.x
- Required Python modules: `sqlite3`, `bcrypt`, `cryptography`, `getpass`



## Usage

Run the script:
```bash
python password_manager.py
```

### Menu Options

1. **Insert New Credentials**
   - Prompts for the master password twice for confirmation.
   - Asks for service name, email, password, and optional notes.
   - Encrypts and stores the password in the database.

2. **Search for an Existing Password**
   - Prompts for the master password.
   - Asks for the service name.
   - Displays associated emails and retrieves the password for the selected email.

3. **Modify an Existing Password**
   - Prompts for the master password.
   - Asks for the old service name, email, and password.
   - Asks for the new service name, email, password, and optional notes.
   - Updates the entry in the database.

4. **Delete an Existing Password**
   - Prompts for the master password.
   - Asks for the service name, email, and password for confirmation.
   - Deletes the entry from the database.

5. **View All Entries in the Database**
   - Prompts for the master password.
   - Displays all stored entries.

6. **Find Services by Email**
   - Prompts for the master password.
   - Asks for the email.
   - Displays all services associated with the given email.

7. **Delete All Entries**
   - Prompts for the master password.
   - Asks for confirmation before deleting all entries.

### Important Notes

- **Master Password**: Each database should use a single master password for consistency. The master password is not stored anywhere and must be remembered by the user. It is unique for each user.
- **Data Integrity**: Entering an incorrect master password when adding or modifying an entry can corrupt the database.
- **Irreversible Actions**: Deleting entries or the entire database is irreversible. Ensure you have the correct master password and service details before performing these actions.
- **Encryption**: Passwords are encrypted using the `cryptography.fernet` module with AES encryption.
- **Salt**: A unique salt is generated for each password entry to ensure security.
- **Master Password Input**: For every operation, you will be prompted to enter the master password. If the master password is entered incorrectly, the program will return an error and allow you to repeat the operation, except when inserting a new password (option 1). In this case, the master password must be entered twice for confirmation.
- **Critical Warning**: Entering the wrong master password when inserting data can irreversibly damage the entire database.
- **Service Input**: Service inputs are converted to lowercase for more friendly searches. Other fields like master password, email/account name, password, and notes are case sensitive.
- **Password Input**: The `strip()` method is used for password inputs to remove any leading or trailing spaces or tabs.
- **Uniqueness Constraint**: The same service with the same account cannot be inserted multiple times, even with different passwords.


### Security Considerations

- **Encryption**: Utilizes the `cryptography.fernet` module with AES in CBC mode and an HMAC to ensure message integrity.
- **Key Generation**: Uses the master password and a unique salt to generate encryption keys.
- **Data Security**: Ensures that passwords are securely encrypted and only accessible with the correct master password.
