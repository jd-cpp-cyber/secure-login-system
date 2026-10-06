# Secure Login & Password Hashing System

A Flask-based secure authentication system built with Python and SQLite.

This project demonstrates secure user registration, password hashing, login authentication, session management, and basic database security practices.

## Features

* User registration with password hashing
* Secure password verification during login
* SQLite database for storing user accounts
* Session-based authentication
* Protected dashboard for authenticated users
* Logout functionality
* Duplicate username detection
* Parameterized SQL queries to reduce SQL injection risk
* Environment-based secret key configuration

## Technologies Used

* Python 3
* Flask
* SQLite
* Werkzeug Security
* HTML5
* Git & GitHub

## Security Features

### Password Hashing

User passwords are never stored as plain text. Passwords are hashed using Werkzeug's secure password hashing functions before being stored in the database.

### Password Verification

During login, the submitted password is verified against the stored password hash using `check_password_hash()`.

### SQL Injection Protection

Parameterized SQL queries are used when interacting with the SQLite database instead of directly inserting user input into SQL statements.

### Session Authentication

Flask sessions are used to keep track of authenticated users and protect the dashboard from unauthenticated access.

### Sensitive File Protection

The local database and virtual environment are excluded from Git using `.gitignore`.

## Project Structure

```text
secure-login-system/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── login.html
│   └── register.html
└── static/
```

`users.db` and `venv/` are created locally but excluded from GitHub using `.gitignore`.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/jd-cpp-cyber/secure-login-system.git
cd secure-login-system
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python3 app.py
```

Open the local URL shown in the terminal in your browser.

## Testing

The following authentication scenarios were tested:

* Successful user registration
* Duplicate username detection
* Successful login
* Invalid password handling
* Protected dashboard access
* Logout functionality
* Password hashes stored instead of plaintext passwords

## Future Improvements

* Password strength validation
* Login rate limiting
* CSRF protection
* Improved user interface
* Better error and success messages
* Secure production configuration
* Automated security testing

## Disclaimer

This project was developed for educational purposes to understand secure authentication and basic web application security concepts.


