# FastAPI Authentication Base

This repository serves as a foundational backend project built with FastAPI, SQLAlchemy (ORM), and PostgreSQL, featuring robust user authentication using JSON Web Tokens (JWT) and role-based access control (RBAC). It's designed as a starting point for building scalable and secure web APIs.

## Features

- **FastAPI Framework**: Modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy ORM**: Powerful and flexible Object Relational Mapper for interacting with PostgreSQL.
- **PostgreSQL Database**: Robust and widely used relational database.
- **Alembic Migrations**: Database schema version control to manage database changes.
- **User Management**: Endpoints for creating and retrieving user accounts.
- **Password Hashing**: Secure password storage using Bcrypt.
- **JWT Authentication**: Secure user login and session management using Access Tokens.
- **Role-Based Access Control (RBAC)**: Fine-grained control over API endpoint access based on user roles (e.g., `user`, `hr`, `admin`).
- **Modular API Structure**: Organized `api` endpoints into separate modules (`auth`, `users`) for better maintainability.
- **Pydantic Schemas**: Data validation and serialization for API requests and responses, providing automatic OpenAPI documentation.
- **Environment Configuration**: Secure loading of sensitive settings via `.env` files using `Pydantic-Settings`.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+**: Download from [python.org](https://www.python.org/).
- **PostgreSQL**: Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/).
    - For Debian/Ubuntu, typically:
        ```bash
        sudo apt update
        sudo apt install postgresql postgresql-contrib
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        ```

## Quick Start Guide

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository (or Initialize Locally)

If you have a remote repository:

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/fastapi-auth-base.git](https://github.com/YOUR_GITHUB_USERNAME/fastapi-auth-base.git)
cd fastapi-auth-base
```

If you're starting locally and will connect to GitHub later:
```bash
mkdir fastapi-auth-base
cd fastapi-auth-base
git init
git branch -M main # Ensure your default branch is 'main'
```

### 2. Set up Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.
```bash
python3 -m venv .venv
source .venv/bin/activate
```
You should see (.venv) in your terminal prompt, indicating the environment is active.

### 3. Install Dependencies
Install all required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Database Setup (PostgreSQL)
#### a. Create Database and User
Connect to your PostgreSQL server (e.g., as the postgres user) and create a database and a dedicated user for your application.
```bash
sudo -i -u postgres
psql
```
At the psql prompt:
```bash
CREATE DATABASE learnobots_db;
CREATE USER learnobots_user WITH ENCRYPTED PASSWORD 'your_strong_password';
GRANT ALL PRIVILEGES ON DATABASE learnobots_db TO learnobots_user;
\q
```
Then exit the postgres user shell:
```bash
exit
```
Remember to replace 'your_strong_password' with a secure password.

#### b. Configure Environment Variables (`.env`)
Create a `.env` file in the root of your project directory. This file will store your database connection string and JWT secret key. This file is excluded from Git using `.gitignore` for security.
```bash
touch .env
```
Open .env and add the following, replacing placeholders with your actual details:
```bash
DATABASE_URL="postgresql://learnobots_user:your_strong_password@localhost:5432/learnobots_db"
PROJECT_NAME="Learnobots Job Portal API"
API_V1_STR="/api/v1"
SECRET_KEY="YOUR_GENERATED_JWT_SECRET_KEY" # Generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```
Generate a unique SECRET_KEY!

#### c. Configure Alembic
Alembic is set up to read the `DATABASE_URL` from your environment variables. Ensure the `alembic.ini` and `alembic/env.py` files are configured as follows:
- `alembic.ini`: Find `sqlalchemy.url =` = and set it to `${DATABASE_URL}`.
```bash
# alembic.ini (snippet)
# ...
sqlalchemy.url = ${DATABASE_URL}
# ...
```
- `alembic/env.py`: Ensure `target_metadata` points to `Base` from `app.db.session` and `load_dotenv` is called.
```bash
# alembic/env.py (snippet)
# ...
from app.db.session import Base
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) # This loads variables from .env

target_metadata = Base
# ...
def run_migrations_online():
    url = os.getenv("DATABASE_URL") # Ensure this line fetches from environment
    connectable = engine_from_config(
        {"sqlalchemy.url": url}, # Pass the URL fetched from environment
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    # ... rest of the function
```

#### d. Run Database Migrations
Apply the initial database schema to your PostgreSQL database.
```bash
# Ensure your .env variables are loaded for Alembic, or that alembic/env.py handles it
# If alembic/env.py has load_dotenv(), this step is just:
alembic upgrade head
# Otherwise, you might need:
# export $(grep -v '^#' .env | xargs) && alembic upgrade head
```

### 5. Run the FastAPI Application
From the project root directory (`fastapi-auth-base`), start the Uvicorn server:
```bash
uvicorn app.api.main:app --reload
```
The application will be accessible at http://127.0.0.1:8000.

## API Endpoints & Testing
Once the server is running, you can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`. This interface allows you to explore and test all available endpoints.

All API endpoints are prefixed with `/api/v1`.

### 1. User Management
- **Create User (Public Registration):** `POST /api/v1/users`
    - **Request Body**: `{"email": "your@example.com", "password": "your_strong_password"}`
    - **Purpose:** Register a new user with a default role of "user".

### 2. Authentication
- **Login & Get Token:** `POST /api/v1/auth/token`
    - **Request Body (Form Data):** `username: your@example.com, password: your_strong_password`
    - **Purpose:** Authenticate and receive a JWT `access_token`. Copy this token for authenticated requests.

### 3. Role-Based Access Control (RBAC) Testing
To test RBAC, you'll need users with different roles. Initially, new users are created with `role="user"`.

### Assigning Roles for Testing
You can manually update a user's role in the PostgreSQL database for testing purposes:
1. Connect to your database using `psql`:
```bash
psql -U learnobots_user -d learnobots_db
```

2. Update a user's role (replace with your user's email):
```bash
UPDATE users SET role = 'hr' WHERE email = 'test_hr@example.com';
UPDATE users SET role = 'admin' WHERE email = 'test_admin@example.com';
\q
```

### Testing Protected Endpoints

1. **Authorize in Swagger UI:**
   - Click the **Authorize** button (top right of Swagger UI).
   - In the dialog, enter your `access_token` prefixed with `Bearer ` (e.g., `Bearer eyJ...`).
   - Click **Authorize**, then **Close**.

2. **Test Endpoints:**

   - **Get All Users**  
     `GET /api/v1/users/`  
     **Expected Behavior:**  
     - Unauthenticated: `401 Unauthorized`  
     - Authenticated with **user** role: `403 Forbidden`  
     - Authenticated with **hr** or **admin** role: `200 OK` (returns list of users)

   - **Get User by ID**  
     `GET /api/v1/users/{user_id}`  
     **Expected Behavior:**  
     - Unauthenticated: `401 Unauthorized`  
     - Authenticated with **user** role: `403 Forbidden`  
     - Authenticated with **hr** or **admin** role: `200 OK` (returns specific user details)

## Project Structure
.
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── main.py         # FastAPI app & router incl.
│   │   └── users.py        # User management endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth.py         # JWT utilities
│   │   ├── config.py       # Settings from .env
│   │   └── deps.py         # Auth & RBAC dependencies
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base_class.py   # Declarative base & fields
│   │   ├── models.py       # SQLAlchemy models
│   │   └── session.py      # Engine & session setup
│   └── schemas/
│       ├── __init__.py
│       ├── token.py        # Pydantic JWT schemas
│       └── user.py         # Pydantic user schemas
├── alembic/
│   ├── versions/           # Migration scripts
│   └── env.py              # Alembic env config
├── alembic.ini             # Alembic settings
├── tests/                  # Unit & integration tests
│   └── __init__.py
├── .env                    # Environment variables (ignored)
├── .gitignore              # Git ignore rules
└── requirements.txt        # Project dependencies


## Contributing
Contributions are welcome! Please follow standard Git Flow or GitHub Flow for feature development and bug fixes.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.