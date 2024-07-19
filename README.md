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

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
   ```

2. Install the required Python modules:
   ```bash
   pip install bcrypt cryptography
   ```

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

- **Master Password**: Each database should use a single master password for consistency. The master password is not stored anywhere and must be remembered by the user.
- **Data Integrity**: Entering an incorrect master password when adding or modifying an entry can corrupt the database.
- **Irreversible Actions**: Deleting entries or the entire database is irreversible. Ensure you have the correct master password and service details before performing these actions.

### Security Considerations

- **Encryption**: Passwords are encrypted using the `cryptography.fernet` module with AES encryption.
- **Salt**: A unique salt is generated for each password entry to ensure security.
- **Master Password**: The master password is essential for encrypting and decrypting passwords and should be kept secure.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Contact

For any questions or issues, please open an issue on GitHub or contact me at [your-email@example.com].

---

Thank you for using this password manager! Remember to keep your master password secure and never share it with anyone.
