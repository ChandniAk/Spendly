# Spendly

A simple expense tracker built with Flask.

## Features

- User registration and login
- Add, edit, and delete expenses
- User profile management

> Note: several features are still in progress (logout, profile, and expense management routes).

## Getting Started

### Prerequisites

- Python 3.12+

### Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r expense-tracker/requirements.txt
```

### Run the app

```powershell
python expense-tracker/app.py
```

The app will be available at http://127.0.0.1:5001.

### Run tests

```powershell
pytest
```

## Tech Stack

- [Flask](https://flask.palletsprojects.com/)
- [pytest](https://docs.pytest.org/) / [pytest-flask](https://pytest-flask.readthedocs.io/)
