# Bharat Teleclinic Backend Assignment (Updated)

This repository contains an updated reference implementation for a simple **Tele‑Medicine** backend.  It is written using Python’s `FastAPI` framework.  The project was created as part of a practical exercise for Bharat Tele Clinic to assess backend skills.

## Features

* **User registration and login.**  Clients can create accounts and log in to obtain JSON Web Tokens (JWTs) for subsequent requests.
* **Role based access control.**  Each user can be either a `doctor` or a `patient`.  Doctors and patients can manage their own details through CRUD operations.
* **Appointments API.**  Patients can schedule appointments with doctors, and both parties can view lists of upcoming appointments.
* **Real‑time status via WebSockets.**  Doctors can broadcast their online/offline status to subscribed clients over a WebSocket endpoint.
* **Automatic API documentation.**  FastAPI automatically exposes a Swagger UI at `/docs` and an OpenAPI JSON schema at `/openapi.json`.

## Getting started

### 1. Prerequisites

* **Python 3.10+** (although the code may run on earlier versions, 3.10 was used during development).
* **Virtual environment** (recommended).  You can create one with `python3 -m venv venv`.
* **PostgreSQL** server (optional).  The example uses SQLite by default for simplicity.  To switch to PostgreSQL set the `DATABASE_URL` environment variable as described below.

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Run the application

Launch the development server using Uvicorn:

```sh
python -m uvicorn app.main:app --reload
```

### 4. Configuring the database

The project reads the database URL from the `DATABASE_URL` environment variable.  If this variable is not set an in‑memory SQLite database (`sqlite:///./test.db`) will be used.  To connect to PostgreSQL set `DATABASE_URL`, for example:

```sh
export DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/teleclinic
```

### 5. Running tests (optional)

Basic unit tests for the registration and login endpoints are provided in the `tests` directory.  You can run them using:

```sh
pytest
```

## Code overview

The source code is organised into a small set of modules to keep the responsibilities clear:

| Module             | Purpose                                                    |
|--------------------|------------------------------------------------------------|
| `app/main.py`      | Application entry point and router registration.           |
| `app/database.py`  | SQLAlchemy session creation and database initialisation.  |
| `app/models.py`    | SQLAlchemy models defining the database schema.  Updated with `__allow_unmapped__` to support SQLAlchemy 2.0 typings.          |
| `app/schemas.py`   | Pydantic models used for request/response validation.     |
| `app/security.py`  | Password hashing and JWT token creation/verification.     |
| `app/crud.py`      | Helper functions to query and mutate the database.        |
| `app/deps.py`      | Dependency injection helpers for FastAPI routes.          |
| `app/routers/`     | Individual routers for authentication, users, appointments and WebSockets. |

## License

This code is provided for educational purposes and does not include any warranty.  Feel free to use and adapt it for your learning.