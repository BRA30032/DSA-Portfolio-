# display.py
# All terminal display functions — tables, menus, headers, messages.
# No logic here — only visual formatting.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "data"))

from colors import BOLD, RESET, GREEN, RED, YELLOW, BLUE, CYAN, GREY, WHITE

VALID_STATUSES = ["Pending", "In Progress", "Completed"]

STATUS_COLORS = {
    "Pending":     YELLOW,
    "In Progress": BLUE,
    "Completed":   GREEN,
}


def divider(char="─", width=72):
    print(f"  {BOLD}{char * width}{RESET}")


def print_banner():
    print(f"""
{CYAN}{BOLD}
  ╔══════════════════════════════════════════════════╗
  ║           📚  WELCOME to HOMEWORK TRACKER  📚   ║
  ║              Terminal Edition                    ║
  ╚══════════════════════════════════════════════════╝
{RESET}""")


def print_success(msg: str):
    print(f"\n  {GREEN}✔  {msg}{RESET}\n")


def print_error(msg: str):
    print(f"\n  {RED}✘  {msg}{RESET}\n")


def print_info(msg: str):
    print(f"  {GREY}{msg}{RESET}")


def print_section(title: str):
    print()
    divider()
    print(f"  {BOLD}{CYAN}{title}{RESET}")
    divider()
    print()


def prompt(label: str) -> str:
    return input(f"  {BOLD}{label}:{RESET} ").strip()


def prompt_menu(label: str) -> str:
    return input(f"\n  {BOLD}» Enter choice [{label}]:{RESET} ").strip()


def print_menu(title: str, options: list):
    print()
    divider("─", 50)
    print(f"  {BOLD}{CYAN}{title}{RESET}")
    divider("─", 50)
    for i, option in enumerate(options, 1):
        print(f"  {CYAN}[{i}]{RESET}  {option}")
    divider("─", 50)


def print_homework_table(entries: list, title: str = "Homework List"):
    if not entries:
        print_error("No homework records found.")
        return

    print_section(title)
    print(f"  {BOLD}{'ID':<10}{'SUBJECT':<18}{'DATE GIVEN':<14}{'DUE DATE':<14}{'STATUS':<16}DESCRIPTION{RESET}")
    print(f"  {'─'*10}{'─'*18}{'─'*14}{'─'*14}{'─'*16}{'─'*30}")

    for e in entries:
        color  = STATUS_COLORS.get(e["status"], RESET)
        desc   = e["description"][:32] + "..." if len(e["description"]) > 32 else e["description"]
        print(f"  {CYAN}{e['id']:<10}{RESET}"
              f"{e['subject']:<18}"
              f"{e['date_given']:<14}"
              f"{e['due_date']:<14}"
              f"{color}{e['status']:<16}{RESET}"
              f"{desc}")
    print()
    print_info(f"  Total: {len(entries)} record(s)")
    print()


def print_homework_detail(entry: dict):
    color = STATUS_COLORS.get(entry["status"], RESET)
    print()
    divider("─", 52)
    print(f"  {BOLD}Homework Detail  —  {CYAN}{entry['id']}{RESET}")
    divider("─", 52)
    print(f"  {'Subject':<18}: {entry['subject']}")
    print(f"  {'Date Given':<18}: {entry['date_given']}")
    print(f"  {'Due Date':<18}: {entry['due_date']}")
    print(f"  {'Status':<18}: {color}{entry['status']}{RESET}")
    print(f"  {'Added On':<18}: {entry['created_at']}")
    print(f"  {'Description':<18}:")
    print(f"    {entry['description']}")
    divider("─", 52)
    print()


def print_status_options():
    print()
    for i, s in enumerate(VALID_STATUSES, 1):
        color = STATUS_COLORS.get(s, RESET)
        print(f"  {CYAN}[{i}]{RESET}  {color}{s}{RESET}")
    print()
