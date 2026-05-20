# user_manager.py
# Handles all user registration, login, and user database access.
# User data is stored in data/users.json

import json
import hashlib
import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def _ensure_data_dir():
    """Create the data folder and users.json if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _load_users() -> dict:
    _ensure_data_dir()
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(users: dict):
    _ensure_data_dir()
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def user_exists(username: str) -> bool:
    return username.lower() in _load_users()


def register_user(name: str, username: str, password: str):
    users = _load_users()
    if username.lower() in users:
        return False, "Username already exists. Please choose a different one."
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(password) < 4:
        return False, "Password must be at least 4 characters long."
    users[username.lower()] = {
        "name":     name.strip(),
        "username": username.lower(),
        "password": _hash_password(password),
    }
    _save_users(users)
    return True, f"Account created successfully! Welcome, {name}!"


def login_user(username: str, password: str):
    users = _load_users()
    key   = username.lower()
    if key not in users:
        return False, "Username not found. Please check and try again.", {}
    if users[key]["password"] != _hash_password(password):
        return False, "Incorrect password. Please try again.", {}
    return True, f"Welcome back, {users[key]['name']}!", users[key]


def get_user(username: str) -> dict:
    return _load_users().get(username.lower(), {})
