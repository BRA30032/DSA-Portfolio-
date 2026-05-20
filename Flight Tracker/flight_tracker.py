# flight_tracker.py
# handles all display and user interaction.
# All logic is taken from logic.py. All data is taken from data files.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
from colors import BOLD, CYAN, GREY, RED, RESET, STATUS_COLORS
from logic import (
    find_airport,
    generate_flights,
    get_flight_by_number,
    build_google_link,
    get_all_airports_list,
)


# ── Display functions ─────────────────────────────────────────────────────────

def print_header(airport: dict):
    print()
    print(f"{BOLD}{'─' * 82}{RESET}")
    print(f"  {BOLD}{CYAN}✈  {airport['code']}  —  {airport['name']}{RESET}")
    print(f"     {airport['city']}, {airport['country']}")
    print(f"{BOLD}{'─' * 82}{RESET}")


def print_flights(flights: list, flight_type: str):
    from datetime import datetime
    label   = "ARRIVALS" if flight_type == "arrivals" else "DEPARTURES"
    now_str = datetime.now().strftime("%H:%M")

    print(f"\n  {BOLD}{label}{RESET}  {GREY}(as of {now_str}){RESET}\n")

    if flight_type == "arrivals":
        print(f"  {BOLD}{'FLIGHT':<9}{'AIRLINE':<26}{'ORIGIN':<18}{'SCHED':<8}{'EST':<12}{'TERMINAL':<12}{'BELT':<7}STATUS{RESET}")
        print(f"  {'─'*9}{'─'*26}{'─'*18}{'─'*8}{'─'*12}{'─'*12}{'─'*7}{'─'*14}")
    else:
        print(f"  {BOLD}{'FLIGHT':<9}{'AIRLINE':<26}{'DESTINATION':<18}{'SCHED':<8}{'EST':<12}{'TERMINAL':<12}STATUS{RESET}")
        print(f"  {'─'*9}{'─'*26}{'─'*18}{'─'*8}{'─'*12}{'─'*12}{'─'*14}")

    for f in flights:
        color    = STATUS_COLORS.get(f["status"], RESET)
        est_str  = f["est"] + (f"  {RED}+{f['delay']}m{RESET}" if f["delay"] > 0 else "")
        t_gate   = f"{f['terminal']}/{f['gate']}"

        if flight_type == "arrivals":
            print(f"  {CYAN}{f['flight']:<9}{RESET}"
                  f"{f['airline']:<26}"
                  f"{f['place']:<18}"
                  f"{f['sched']:<8}"
                  f"{est_str:<12}"
                  f"{t_gate:<12}"
                  f"{f['belt']:<7}"
                  f"{color}{f['status']}{RESET}")
        else:
            print(f"  {CYAN}{f['flight']:<9}{RESET}"
                  f"{f['airline']:<26}"
                  f"{f['place']:<18}"
                  f"{f['sched']:<8}"
                  f"{est_str:<12}"
                  f"{t_gate:<12}"
                  f"{color}{f['status']}{RESET}")
    print()


def print_flight_detail(flight: dict, flight_type: str):
    color = STATUS_COLORS.get(flight["status"], RESET)
    label = "Origin" if flight_type == "arrivals" else "Destination"
    link  = build_google_link(flight)

    print(f"\n  {BOLD}{'─' * 52}{RESET}")
    print(f"  {BOLD}Flight Detail  —  {CYAN}{flight['flight']}{RESET}")
    print(f"  {'─' * 52}")
    print(f"  {'Airline':<18}: {flight['airline']}")
    print(f"  {'Aircraft':<18}: {flight['aircraft']}")
    print(f"  {label:<18}: {flight['place']}")
    print(f"  {'Scheduled':<18}: {flight['sched']}")
    est_line = flight["est"]
    if flight["delay"] > 0:
        est_line += f"  {RED}(+{flight['delay']} min delay){RESET}"
    print(f"  {'Estimated':<18}: {est_line}")
    print(f"  {'Terminal / Gate':<18}: {flight['terminal']} / {flight['gate']}")
    if flight_type == "arrivals":
        print(f"  {'Baggage Belt':<18}: {flight['belt']}")
    print(f"  {'Status':<18}: {color}{flight['status']}{RESET}")
    print(f"\n  {GREY}Google: {link}{RESET}")
    print(f"  {BOLD}{'─' * 52}{RESET}\n")


def print_airport_list():
    airports = get_all_airports_list()
    print(f"\n  {BOLD}Supported Airports:{RESET}\n")
    for i in range(0, len(airports), 3):
        row  = airports[i:i + 3]
        line = "   ".join(f"{CYAN}{code}{RESET}  {city:<30}" for code, city in row)
        print(f"  {line}")
    print()


def print_help():
    print(f"""
  {BOLD}Commands:{RESET}
    {CYAN}<airport>{RESET}       Search by  code or city  (e.g. MAA, SIN, Dubai, London)
    {CYAN}list{RESET}            Show all supported airports
    {CYAN}help{RESET}            Show this help message
    {CYAN}exit / quit{RESET}     Exit the app
""")


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}{CYAN}  ✈  Flight Tracker  —  Terminal Edition{RESET}")
    print(f"  {GREY}Type an airport code or city name to get started.{RESET}")
    print_help()

    while True:
        try:
            user_input = input(f"{BOLD}flight-tracker>{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {GREY}Goodbye! ✈{RESET}\n")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ("exit", "quit", "q"):
            print(f"\n  {GREY}Goodbye! ✈{RESET}\n")
            break

        elif cmd == "help":
            print_help()

        elif cmd == "list":
            print_airport_list()

        else:
            airport = find_airport(user_input)
            if not airport:
                print(f"\n  {RED}Airport not found for '{user_input}'.{RESET}  "
                      f"Type {CYAN}list{RESET} to see all supported airports.\n")
                continue

            arrivals   = generate_flights(airport, "arrivals")
            departures = generate_flights(airport, "departures")

            print_header(airport)
            print_flights(arrivals, "arrivals")
            print_flights(departures, "departures")

            # Flight detail lookup
            while True:
                detail_input = input(
                    f"  {GREY}Enter a flight number for details, or press Enter to search again:{RESET} "
                ).strip()

                if not detail_input:
                    break

                flight, ftype = get_flight_by_number(detail_input, arrivals, departures)
                if flight:
                    print_flight_detail(flight, ftype)
                else:
                    print(f"  {RED}Flight '{detail_input.upper()}' not found in current results.{RESET}\n")
                    break


if __name__ == "__main__":
    main()
