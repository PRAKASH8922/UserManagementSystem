## 🌐 Live Demo

**Available at your primary URL:**

https://usermanagementsystem-zxl5.onrender.com


# User Management System (Django + MySQL)

A fullstack User Management System developed using **Python, Django, HTML, CSS, JavaScript, and MySQL**, converted faithfully from the original reference architecture.

## Features

- **User Registration (`/signup.html`)**:
  - Validates full name, email, phone number (exactly 10 digits), and password confirmation.
  - Strong password policy enforcement (minimum 8 characters, at least 1 uppercase letter, 1 number, and 1 special character).
  - Password visibility toggle (show/hide eye icon).
  - Verifies email uniqueness prior to registration.
  - Securely hashes passwords using Django's PBKDF2 algorithm before saving to the database.

- **User Authentication (`/login.html`)**:
  - Validates email and password credentials.
  - Verifies against stored PBKDF2 password hashes (with transparent upgrade path for legacy entries).
  - Session storage management (`sessionStorage.setItem("userLoggedIn", "true")`).
  - Password visibility toggle.

- **Dashboard & User Management (`/index.html`)**:
  - Protected access: checks active session on page load; redirects unauthorized users to `/login.html`.
  - Tabular view of all registered users (`S.no`, `Name`, `Ph-no`, `Email`, `Edit`, `Delete`).
  - Add new user form.
  - Inline edit: loads selected user data, hides table, switches form to update mode, and updates record.
  - Inline delete: prompts confirmation dialog and deletes record.
  - Logout functionality: clears session storage, alerts the user, and redirects to login.

- **Security & Data Integrity**:
  - Passwords are never returned in plain text or in API responses.
  - Database credentials are kept strictly in environment variables (`.env`).


## Tech Stack

- **Backend**: Python 3.14+, Django 6.1+, PyMySQL
- **Database**: MySQL 8.0+ (`ct_db` database, `ct_user_details` table)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Boxicons CDN
- **Configuration**: `python-dotenv` for environment management


## Project Structure

```
UserManagementSystem/
├── manage.py
├── requirements.txt
├── .gitignore
├── .env.example
├── .env                          # Local database configuration (not committed to VCS)
├── README.md
├── user_management/              # Django project settings
│   ├── __init__.py               # PyMySQL as MySQLdb hook
│   ├── settings.py               # Environment-driven database configuration
│   ├── urls.py                   # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── users/                        # User management application
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                 # CtUserDetails model mapping to 'ct_user_details'
│   ├── user.py                   # User class helper
│   ├── views.py                  # Page and REST API views
│   ├── urls.py                   # REST API routes and page URLs
│   ├── tests.py                  # Automated test suite
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py       # Database migration for ct_user_details
├── templates/                    # HTML Templates
│   ├── index.html                # Protected dashboard
│   ├── login.html                # Login page
│   └── signup.html               # Registration page
└── static/
    ├── css/
    │   └── style.css             # Application stylesheet
    └── js/
        └── script.js             # Client-side workflows and API integration
```

## Prerequisites

1. **Python 3.10+** (Tested with Python 3.14)
2. **MySQL Server 8.0+** running locally (e.g. `MySQL80` service on Windows)

## Installation & Setup

### 1. Clone or Open the Repository
```bash
cd "UserManagementSystem"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MySQL & Environment Variables
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

Open `.env` in a text editor and enter your MySQL root password and connection details:
```env
# Django Configuration
SECRET_KEY=django-insecure-ct-user-management-secret-key-change-in-production
DEBUG=True

# MySQL Database Configuration
DB_NAME=ct_db
DB_USER=root
DB_PASSWORD=YOUR_ACTUAL_MYSQL_PASSWORD
DB_HOST=localhost
DB_PORT=3306
```

### 4. Create the MySQL Database
Log into MySQL and create the `ct_db` database:
```sql
CREATE DATABASE IF NOT EXISTS ct_db;
```

### 5. Apply Migrations
Apply the initial migration to create the `ct_user_details` table:
```bash
python manage.py migrate
```

## Running the Application

Start the Django development server:
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Home / Dashboard**: `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/index.html`
- **Login**: `http://127.0.0.1:8000/login.html`
- **Signup**: `http://127.0.0.1:8000/signup.html`

## Running Tests

Execute the automated test suite:
```bash
python manage.py test
```
All tests verify endpoints, status codes, password hashing, and user authentication workflows.

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/user` | Returns list of all registered users (excluding password) |
| `POST` | `/user` | Registers/creates a new user with PBKDF2 hashed password |
| `PUT` | `/user/<id>` | Updates an existing user's details |
| `DELETE` | `/user/<id>` | Deletes a user by id |
| `POST` | `/user/login` | Validates credentials against hashed passwords |
