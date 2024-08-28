# Password Manager

![image](https://github.com/user-attachments/assets/7aeaba95-b962-4175-8fee-104d0d34644d)

## Overview

This project is a password manager application developed in Python, featuring a GUI interface for enhanced user convenience and accessibility. The GUI is implemented using `tkinter`, and all core functionalities are designed to ensure a seamless and consistent user experience.

Passwords are securely encrypted using the `cryptography.fernet` module, which employs AES encryption. The master password is used solely to generate encryption keys and is never stored in the database. The database is now hosted on an Aiven server, allowing users to securely access their passwords from multiple devices with ease. Multiple user accounts are supported, each with its own encrypted database.

The application can be packaged into an executable file (`pm_gui.exe`) using the following command:  
```bash
pyinstaller pm_gui.py --onefile --noconsole
```
Users can navigate between different features using the buttons at the top of the GUI or by pressing function keys F1-F9. When one or more passwords are displayed, users can copy the desired password to the clipboard for easy pasting.

## Features

- **Account Registration**: Users register with a unique username and master password. The master password is used to encrypt the database name specific to each user, ensuring data isolation.
- **Add Passwords**: Store new passwords securely in the database.
- **Retrieve Passwords**: Retrieve passwords for specified services and accounts.
- **Modify Passwords**: Update existing passwords and associated details.
- **Delete Passwords**: Remove specific passwords from the database.
- **View All Entries**: Display all stored passwords.
- **Find Services by Email**: List all services associated with a particular email.
- **Delete All Entries**: Remove all entries from the database.
- **Credit Card Management**: Securely add, search, and delete credit card information, ensuring sensitive card details are protected.

## Database Hosting

The application uses a cloud-hosted database powered by **Aiven**, enabling users to:

- Access their data across multiple devices.
- Maintain multiple user accounts, with each account's data isolated in its own encrypted database.
- Register using a unique username and master password. The master password is crucial for encryption and is never stored.

During registration, the master password is used to encrypt the name of the user’s specific database, ensuring that each user’s information remains private and secure.

### Important Notes:
- Users must remember their master password, as it is not stored anywhere and is required to access their database.
- If the master password is lost, the user will not be able to access their data.
  
## Menu Options

### Register New Account

- Asks for a unique username.
- Prompts for the master password twice for confirmation.
- Creates a new encrypted database for the user on the Aiven server.

### Insert New Credentials

- Prompts for the master password.
- Asks for service name, email, password, and optional notes.
- Encrypts and stores the password in the user's personal database.

### Search for an Existing Password

- Prompts for the master password.
- Asks for the service name.
- Displays associated emails and retrieves the password for the selected email.
- Copies the password to the clipboard automatically.

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
- Displays all stored entries for the user.

### Find Services by Email

- Prompts for the master password.
- Asks for the email.
- Displays all services associated with the given email.

### Delete All Entries

- Prompts for the master password.
- Asks for confirmation before deleting all entries in the user's personal database.

### Credit Card Management

- Prompts for card details such as card number, expiry date, CVV, and associated email. Encrypts and stores this information in the user's database.
- Prompts for the master password and card details. Retrieves and displays the credit card information associated with the given email or card number.
- Prompts for the master password, email, and card number for confirmation. Deletes the credit card entry from the database.

  **Important Note**: Credit cards cannot be modified once added. This is a security measure since banks do not allow the modification of individual elements like CVV or card numbers. If card details change, users must delete the old entry and add a new one.

## Security Considerations

### Encryption

- Passwords are encrypted using the `cryptography.fernet` module with AES encryption.
- The master password and a unique random salt are used to generate encryption keys for each user’s database.
- Keys are generated using **pbkdf2_hmac** funcions, which is set to iterate 100000 and creates a 256bit (32bytes) key. **PBKDF2** with **SHA-256** is used to generate keys, that are then used in simmetric encryption with **AES**
```python
    def generate_key(password, salt):
      password = password.encode()
      key = hashlib.pbkdf2_hmac('sha256', password, salt, 100000, dklen=32)
      return base64.urlsafe_b64encode(key)
  ```
### Data Security

- The master password is never stored in the system. Each user must remember it to access their data.
- Passwords and credit card details are securely encrypted and only accessible with the correct master password.

### Database Access

- Each user’s data is stored in a separate encrypted database hosted on an Aiven server. 
- The database name is encrypted using the master password during registration to ensure user privacy and data isolation.

### Login and Data Flow

1. **Account Registration**: A new account is created with a unique username and master password. The master password is used to encrypt the user’s database name.
2. **Login**: The user logs in with their username and master password. The password decrypts the database name, providing access to the user's information.
3. **Database Operations**: All operations (e.g., adding, retrieving, modifying passwords) are performed on the user-specific encrypted database.

This structure ensures that even if multiple users are accessing the application, their data remains isolated and encrypted.

Simple scheme of Login/Signup:
![login](image.png)

### Error Handling

- The GUI displays error messages and confirmations to guide users through successful operations and troubleshooting.

### Important Considerations

- **Data Integrity**: Entering an incorrect master password when adding or modifying an entry can corrupt the database.
- **Irreversible Actions**: Deleting entries or the entire database is irreversible. Ensure you have the correct master password and service details before performing these actions.
- **Master Password**: Each user must remember their master password, as it is the key to their encrypted database. There is no way to recover the password once lost.

By implementing a secure, cloud-hosted database and robust encryption, this password manager allows users to manage their credentials across multiple devices while maintaining a high level of data security.