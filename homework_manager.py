# homework_manager.py
# All homework creation, retrieval, filtering, and status updates.
# Data stored in data/homework.json

import json
import os
import uuid
from datetime import datetime, timedelta

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
DATA_DIR       = os.path.join(BASE_DIR, "data")
HOMEWORK_FILE  = os.path.join(DATA_DIR, "homework.json")
VALID_STATUSES = ["Pending", "In Progress", "Completed"]
DATE_FORMAT    = "%d-%m-%Y"


def _ensure_data_dir():
    """Create the data folder and homework.json if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(HOMEWORK_FILE):
        with open(HOMEWORK_FILE, "w") as f:
            json.dump({}, f)


def _load_homework() -> dict:
    _ensure_data_dir()
    with open(HOMEWORK_FILE, "r") as f:
        return json.load(f)


def _save_homework(data: dict):
    _ensure_data_dir()
    with open(HOMEWORK_FILE, "w") as f:
        json.dump(data, f, indent=4)


def _get_user_homework(username: str) -> list:
    return _load_homework().get(username.lower(), [])


def _save_user_homework(username: str, entries: list):
    data = _load_homework()
    data[username.lower()] = entries
    _save_homework(data)


def parse_date(date_str: str):
    try:
        return datetime.strptime(date_str.strip(), DATE_FORMAT)
    except ValueError:
        return None


def format_date(dt: datetime) -> str:
    return dt.strftime(DATE_FORMAT)


def add_homework(username, subject, date_given, description, due_date, status):
    if not parse_date(date_given):
        return False, "Invalid 'Date Given'. Use DD-MM-YYYY format."
    if not parse_date(due_date):
        return False, "Invalid 'Due Date'. Use DD-MM-YYYY format."
    if status not in VALID_STATUSES:
        return False, f"Invalid status. Choose from: {', '.join(VALID_STATUSES)}"

    entries = _get_user_homework(username)
    entry = {
        "id":          str(uuid.uuid4())[:8].upper(),
        "subject":     subject.strip(),
        "date_given":  date_given.strip(),
        "description": description.strip(),
        "due_date":    due_date.strip(),
        "status":      status,
        "created_at":  datetime.now().strftime("%d-%m-%Y %H:%M"),
    }
    entries.append(entry)
    _save_user_homework(username, entries)
    return True, f"Homework added! (ID: {entry['id']})"


def get_all_homework(username: str) -> list:
    return _get_user_homework(username)


def get_by_subject(username: str, subject: str) -> list:
    return [e for e in _get_user_homework(username) if subject.lower() in e["subject"].lower()]


def get_by_date(username: str, date_str: str) -> list:
    return [e for e in _get_user_homework(username) if e["due_date"] == date_str.strip()]


def get_by_status(username: str, status: str) -> list:
    return [e for e in _get_user_homework(username) if e["status"].lower() == status.lower()]


def get_by_date_range(username: str, days: int) -> list:
    cutoff  = datetime.now() - timedelta(days=days)
    results = []
    for e in _get_user_homework(username):
        dt = parse_date(e["date_given"])
        if dt and dt >= cutoff:
            results.append(e)
    return results


def update_status(username: str, homework_id: str, new_status: str):
    if new_status not in VALID_STATUSES:
        return False, f"Invalid status. Choose from: {', '.join(VALID_STATUSES)}"
    entries = _get_user_homework(username)
    for entry in entries:
        if entry["id"] == homework_id.upper():
            entry["status"] = new_status
            _save_user_homework(username, entries)
            return True, f"Homework {homework_id} updated to '{new_status}'."
    return False, f"No homework found with ID: {homework_id}"


def get_homework_by_id(username: str, homework_id: str):
    for entry in _get_user_homework(username):
        if entry["id"] == homework_id.upper():
            return entry
    return None
