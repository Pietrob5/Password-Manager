# Password Manager

## Overview

This project is a password manager application written in Python. It supports both CLI and GUI interfaces, making it versatile and user-friendly. The GUI is built using `tkinter`, and all core functions are consistent across both interfaces, ensuring seamless functionality regardless of the interface used. Passwords are securely encrypted using the `cryptography.fernet` module, employing AES encryption. The master password generates encryption keys and is never stored in the database. Using pynstaller is possiblme to easily create pm_gui.exe.

![image](https://github.com/user-attachments/assets/bb4c1894-66e5-4ae4-9057-e00ac824d3bb)


## Features

- **Add Passwords**: Store new passwords securely in the database through both CLI and GUI.
- **Retrieve Passwords**: Retrieve passwords for specified services and accounts.
- **Modify Passwords**: Update existing passwords and associated details.
- **Delete Passwords**: Remove specific passwords from the database.
- **View All Entries**: Display all stored passwords.
- **Find Services by Email**: List all services associated with a particular email.
- **Delete All Entries**: Remove all entries from the database.

## Menu Options

### Insert New Credentials

- Prompts for the master password twice for confirmation.
- Asks for service name, email, password, and optional notes.
- Encrypts and stores the password in the database.

### Search for an Existing Password

- Prompts for the master password.
- Asks for the service name.
- Displays associated emails and retrieves the password for the selected email.
- Copies the password to clipboard automatically.

### Modify an Existing Password

- Prompts for the master password.
- Asks for the old service name, email, and password.
- Asks for the new service name, email, password, and optional notes.
- Updates the entry in the database.

### Delete an Existing Password

- Prompts for the master password.
- Asks for the service name, email, and password for confirmation.
- Deletes the entry from the database.

### View All Entries in the Database

- Prompts for the master password.
- Displays all stored entries.

### Find Services by Email

- Prompts for the master password.
- Asks for the email.
- Displays all services associated with the given email.

### Delete All Entries

- Prompts for the master password.
- Asks for confirmation before deleting all entries.

## Important Notes

### Master Password

- Each database should use a single master password for consistency. The master password is not stored anywhere and must be remembered by the user. It is unique for each user.

### Data Integrity

- Entering an incorrect master password when adding or modifying an entry can corrupt the database.

### Irreversible Actions

- Deleting entries or the entire database is irreversible. Ensure you have the correct master password and service details before performing these actions.

### Encryption

- Passwords are encrypted using the `cryptography.fernet` module with AES encryption.

### Salt

- A unique salt is generated for each password entry to ensure security.

### Master Password Input

- For every operation, you will be prompted to enter the master password. If the master password is entered incorrectly, the program will return an error and allow you to repeat the operation, except when inserting a new password (option 1). In this case, the master password must be entered twice for confirmation.
- Critical Warning: Entering the wrong master password when inserting data can irreversibly damage the entire database.

### Service Input

- Service inputs are converted to lowercase for more friendly searches. Other fields like master password, email/account name, password, and notes are case sensitive.

### Input Fields

- The `strip()` method is used for all inputs to remove any leading or trailing spaces or tabs. `lower()` is used for service names to avoid mistyping by the user.

### Uniqueness Constraint

- The same service with the same account cannot be inserted multiple times, even with different passwords.

## Security Considerations

### Encryption

- Utilizes the `cryptography.fernet` module with AES in CBC mode and an HMAC to ensure message integrity.

### Key Generation

- Uses the master password and a unique salt to generate encryption keys.

### Data Security

- Ensures that passwords are securely encrypted and only accessible with the correct master password.

### Graphical User Interface (GUI)

- The program now includes a GUI to enhance user experience. Users can perform all the aforementioned operations through an intuitive interface.
- **Features**: The GUI includes buttons and fields for each operation (Add, Retrieve, Modify, Delete, etc.), providing a more accessible and user-friendly way to manage passwords.
- **Error Handling**: The GUI displays error messages and confirmations, guiding users through successful operations and troubleshooting.
