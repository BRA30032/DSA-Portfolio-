# main.py
# Entry point — all menus and user flow.

import sys
import os
import getpass


BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
DATA_DIR = os.path.join(BASE_DIR, "data")
sys.path.insert(0, BASE_DIR)   
sys.path.insert(0, DATA_DIR)   
# ───────────────────────────────────────────────────────────────────────────

from colors import BOLD, RESET, GREEN, RED, CYAN, GREY, YELLOW
from user_manager import register_user, login_user
from homework_manager import (
    add_homework, get_all_homework, get_by_subject,
    get_by_date, get_by_status, get_by_date_range,
    update_status, get_homework_by_id, VALID_STATUSES, parse_date
)
from display import (
    print_banner, print_menu, print_section, print_success,
    print_error, print_info, prompt, prompt_menu,
    print_homework_table, print_homework_detail,
    print_status_options, divider
)


# ── Auth ───────────────────────────────────────────────────────────────────────

def screen_new_user():
    print_section("CREATE NEW ACCOUNT")

    name = prompt("Full Name")
    if not name:
        print_error("Name cannot be empty.")
        return None

    username = prompt("Choose Username")
    if not username:
        print_error("Username cannot be empty.")
        return None

    password = getpass.getpass(f"  {BOLD}Choose Password:{RESET} ")
    if not password:
        print_error("Password cannot be empty.")
        return None

    success, message = register_user(name, username, password)
    if success:
        print_success(message)
        return {"name": name, "username": username.lower()}
    else:
        print_error(message)
        return None


def screen_existing_user():
    print_section("LOGIN")

    username = prompt("Username")
    if not username:
        print_error("Username cannot be empty.")
        return None

    password = getpass.getpass(f"  {BOLD}Password:{RESET} ")

    success, message, user_data = login_user(username, password)
    if success:
        print_success(message)
        return user_data
    else:
        print_error(message)
        return None


def screen_auth():
    print_menu("Welcome — Are you a new or existing user?", [
        "Existing User  (Login)",
        "New User       (Register)",
        "Exit",
    ])
    choice = prompt_menu("1-3")

    if choice == "1":
        return screen_existing_user()
    elif choice == "2":
        return screen_new_user()
    elif choice == "3":
        return None
    else:
        print_error("Invalid choice. Enter 1, 2 or 3.")
        return screen_auth()


# ── Create Homework ────────────────────────────────────────────────────────────

def screen_create_homework(username):
    print_section("ADD NEW HOMEWORK")

    subject = prompt("Subject  (e.g. Maths, Science)")
    if not subject:
        print_error("Subject cannot be empty.")
        return

    while True:
        date_given_str = prompt("Date Given  (DD-MM-YYYY)")
        if parse_date(date_given_str):
            break
        print_error("Invalid date. Use DD-MM-YYYY  e.g. 24-04-2026")

    description = prompt("Description of Homework")
    if not description:
        print_error("Description cannot be empty.")
        return

    while True:
        due_date_str = prompt("Due Date  (DD-MM-YYYY)")
        if parse_date(due_date_str):
            break
        print_error("Invalid date. Use DD-MM-YYYY  e.g. 30-04-2026")

    print_info("\n  Select Status:")
    print_status_options()
    status_choice = prompt_menu("1-3")
    status_map    = {"1": "Pending", "2": "In Progress", "3": "Completed"}
    status        = status_map.get(status_choice, "Pending")

    success, message = add_homework(
        username, subject, date_given_str,
        description, due_date_str, status
    )
    if success:
        print_success(message)
    else:
        print_error(message)


# ── View Homework ──────────────────────────────────────────────────────────────

def screen_view_by_subject(username):
    subject = prompt("Enter Subject to search")
    if not subject:
        print_error("Subject cannot be empty.")
        return
    results = get_by_subject(username, subject)
    print_homework_table(results, f"Homework — Subject: {subject}")


def screen_view_by_date(username):
    while True:
        date_str = prompt("Enter Due Date  (DD-MM-YYYY)")
        if parse_date(date_str):
            break
        print_error("Invalid date. Use DD-MM-YYYY format.")
    results = get_by_date(username, date_str)
    print_homework_table(results, f"Homework — Due Date: {date_str}")


def screen_view_by_status(username):
    print_info("\n  Select Status to filter by:")
    print_status_options()
    choice     = prompt_menu("1-3")
    status_map = {"1": "Pending", "2": "In Progress", "3": "Completed"}
    status     = status_map.get(choice)
    if not status:
        print_error("Invalid choice.")
        return
    results = get_by_status(username, status)
    print_homework_table(results, f"Homework — Status: {status}")


def screen_view_by_range(username):
    print_menu("View Homework by Time Range", [
        "Past 7 days   (Last Week)",
        "Past 30 days  (Last Month)",
        "Past 90 days  (Last 3 Months)",
        "All Time",
    ])
    choice    = prompt_menu("1-4")
    range_map = {
        "1": (7,    "Past 7 Days"),
        "2": (30,   "Past 30 Days"),
        "3": (90,   "Past 90 Days"),
        "4": (None, "All Time"),
    }
    if choice not in range_map:
        print_error("Invalid choice.")
        return
    days, label = range_map[choice]
    results     = get_all_homework(username) if days is None else get_by_date_range(username, days)
    print_homework_table(results, f"Homework — {label}")


def screen_view_homework(username):
    print_menu("View Homework — Filter By", [
        "Subject",
        "Due Date",
        "Status",
        "Time Range  (past week / month / all)",
        "All Homework",
        "Back to Main Menu",
    ])
    choice = prompt_menu("1-6")

    if   choice == "1": screen_view_by_subject(username)
    elif choice == "2": screen_view_by_date(username)
    elif choice == "3": screen_view_by_status(username)
    elif choice == "4": screen_view_by_range(username)
    elif choice == "5": print_homework_table(get_all_homework(username), "All Homework")
    elif choice == "6": return
    else: print_error("Invalid choice.")


# ── Update Status ──────────────────────────────────────────────────────────────

def screen_update_status(username):
    print_section("UPDATE HOMEWORK STATUS")

    all_hw = get_all_homework(username)
    if not all_hw:
        print_error("You have no homework entries to update.")
        return

    print_homework_table(all_hw, "Your Homework — Pick an ID to update")

    hw_id = prompt("Enter Homework ID").upper()
    entry = get_homework_by_id(username, hw_id)
    if not entry:
        print_error(f"No homework found with ID: {hw_id}")
        return

    print_homework_detail(entry)
    print_info(f"  Current status: {entry['status']}")
    print_info("  Select new status:")
    print_status_options()

    choice     = prompt_menu("1-3")
    status_map = {"1": "Pending", "2": "In Progress", "3": "Completed"}
    new_status = status_map.get(choice)
    if not new_status:
        print_error("Invalid choice.")
        return

    success, message = update_status(username, hw_id, new_status)
    if success:
        print_success(message)
    else:
        print_error(message)


# ── View Detail ────────────────────────────────────────────────────────────────

def screen_view_detail(username):
    print_section("VIEW HOMEWORK DETAIL")

    all_hw = get_all_homework(username)
    if not all_hw:
        print_error("You have no homework entries.")
        return

    print_homework_table(all_hw, "Your Homework")
    hw_id = prompt("Enter Homework ID to view").upper()
    entry = get_homework_by_id(username, hw_id)

    if not entry:
        print_error(f"No homework found with ID: {hw_id}")
        return

    print_homework_detail(entry)


# ── Main Menu ─────────────────────────────────────────────────────────────────

def main_menu(user):
    username = user["username"]
    name     = user["name"]

    while True:
        print()
        divider()
        print(f"  {BOLD}{CYAN}📚 Homework Tracker{RESET}  —  "
              f"Logged in as {GREEN}{name}{RESET}  {GREY}(@{username}){RESET}")
        divider()

        print_menu("Main Menu", [
            "Create — Add new homework",
            "View   — Browse / filter homework",
            "Update — Change homework status",
            "Detail — View full details of a homework",
            "Logout",
        ])

        choice = prompt_menu("1-5")

        if   choice == "1": screen_create_homework(username)
        elif choice == "2": screen_view_homework(username)
        elif choice == "3": screen_update_status(username)
        elif choice == "4": screen_view_detail(username)
        elif choice == "5":
            print_success(f"Logged out. Goodbye, {name}!")
            break
        else:
            print_error("Invalid choice. Enter a number from 1 to 5.")


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    print_banner()
    while True:
        user = screen_auth()
        if user is None:
            print()
            print_info("Goodbye! 📚")
            print()
            break

        main_menu(user)

        print_menu("What would you like to do?", [
            "Login again / Switch user",
            "Exit",
        ])
        if prompt_menu("1-2") != "1":
            print()
            print_info("Goodbye! 📚")
            print()
            break


if __name__ == "__main__":
    main()
