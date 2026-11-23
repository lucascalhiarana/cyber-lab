
# Password Vault

A command-line password manager built with Python.

The project stores credentials in an encrypted vault protected by a master password.

## Features

- Create and unlock an encrypted vault
- Add credentials
- List stored services
- View stored credentials
- Delete credentials
- Generate secure random passwords
- Encrypt vault data using AES-256-GCM
- Derive encryption keys using Argon2id
- Automated tests with Python unittest

## Technologies

- Python
- cryptography
- argon2-cffi
- JSON
- unittest

## Installation

Clone the repository:

```bash
git clone https://github.com/lucascalhiarana/Password-Vault.git
cd Password-Vault
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

On the first run, the application will ask you to create a master password.

On subsequent runs, enter the master password to unlock the vault.

## Running Tests

Run the automated test suite:

```bash
python -m unittest discover -s tests -v
```

## Security Notes

- Credentials are encrypted before being written to the vault file.
- The master password is not stored in the vault.
- Argon2id is used to derive the encryption key.
- AES-GCM provides encryption and authentication.
- Base64 is used only to represent binary data in JSON. It is not encryption.

This project is an educational portfolio project and has not been independently audited.

## Disclaimer

Use this project for learning and experimentation.

Do not rely on it as your only password manager for sensitive or critical accounts.
