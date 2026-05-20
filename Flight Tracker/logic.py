import random
import re
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
from airports import AIRPORTS
from city_map import CITY_MAP
from flight_data import AIRCRAFTS, GATES, STATUS_POOL


def find_airport(query: str) -> dict | None:
    """
    Find an airport by  code, city name, or partial name.
    Returns a data set with the airport data + its code, or None if not found.
    """
    upper = query.strip().upper()
    if upper in AIRPORTS:
        return {"code": upper, **AIRPORTS[upper]}

    lower = query.strip().lower()
    if lower in CITY_MAP:
        code = CITY_MAP[lower]
        return {"code": code, **AIRPORTS[code]}

    for code, info in AIRPORTS.items():
        if lower in info["city"].lower() or lower in info["name"].lower():
            return {"code": code, **info}

    return None


def make_time(base_h: int, base_m: int, offset_min: int) -> str:
    """
    Calculate a time string (HH:MM) from a base hour/minute plus an offset in minutes.
    Wraps around midnight correctly.
    """
    total = (base_h * 60 + base_m + offset_min) % 1440
    if total < 0:
        total += 1440
    return f"{total // 60:02d}:{total % 60:02d}"


def airline_initials(name: str) -> str:
    """
    Generate a 2-letter flight code prefix from an airline name.
    
    """
    cleaned = re.sub(
        r'\b(Air|Airlines|Airways|International|Asia|Japan)\b',
        '', name, flags=re.IGNORECASE
    ).strip()
    parts    = cleaned.split()
    initials = "".join(w[0].upper() for w in parts if w)[:2]
    return initials or "XX"


def generate_flights(airport: dict, flight_type: str) -> list[dict]:
    """
    Generate a list of 10 flights for the given airport.
    flight_type: 'arrivals' or 'departures'
    Each flight data source contains: flight, airline, place, sched, est,
    status, delay, terminal, gate, belt, aircraft.
    """
    now = datetime.now()
    h, m = now.hour, now.minute
    flights = []

    for i in range(10):
        airline  = random.choice(airport["airlines"])
        dest     = random.choice(airport["destinations"])
        fn       = airline_initials(airline) + str(random.randint(100, 999))
        offset   = (i * 28) - 60
        sched    = make_time(h, m, offset)
        status   = random.choice(STATUS_POOL)
        delay    = random.randint(15, 90) if status == "Delayed" else 0
        est      = make_time(h, m, offset + delay)
        terminal = random.choice(airport["terminals"])
        gate     = random.choice(GATES)
        belt     = str(random.randint(1, 14)) if flight_type == "arrivals" else "-"

        flights.append({
            "flight":   fn,
            "airline":  airline,
            "place":    dest,
            "sched":    sched,
            "est":      est,
            "status":   status,
            "delay":    delay,
            "terminal": terminal,
            "gate":     gate,
            "belt":     belt,
            "aircraft": random.choice(AIRCRAFTS),
        })

    return flights


def get_flight_by_number(flight_number: str, arrivals: list, departures: list) -> tuple[dict | None, str | None]:
    """
    Search for a flight by its number across arrivals and departures.
    Returns (flight_dict, flight_type) or (None, None) if not found.
    """
    for flight in arrivals:
        if flight["flight"] == flight_number.upper():
            return flight, "arrivals"
    for flight in departures:
        if flight["flight"] == flight_number.upper():
            return flight, "departures"
    return None, None


def build_google_link(flight: dict) -> str:
    """
    Build a Google  URL for a given flight.
    """
    query = f"{flight['flight']} {flight['airline']} flight status"
    encoded = query.replace(" ", "+")
    return f"https://www.google.com/search?q={encoded}"


def get_all_airports_list() -> list[tuple[str, str]]:
    """
    Return a sorted list of (Code, 'City, Country')  for display.
    """
    return sorted(
        [(code, f"{info['city']}, {info['country']}") for code, info in AIRPORTS.items()],
        key=lambda x: x[1]
    )
