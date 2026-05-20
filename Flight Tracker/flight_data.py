# flight_data.py
# This is the database file with Static flight-related data — aircraft types, gate codes, and status options.
# All the data and information is taken from interet. This is test data.

AIRCRAFTS = [
    "Boeing 737-800",
    "Boeing 737 MAX 8",
    "Boeing 747-400",
    "Boeing 767-300",
    "Boeing 777-300ER",
    "Boeing 787-9 Dreamliner",
    "Airbus A319",
    "Airbus A320neo",
    "Airbus A321",
    "Airbus A330-300",
    "Airbus A350-900",
    "Airbus A380",
    "Embraer E190",
    "Bombardier CRJ-900",
]

GATES = [
    "A1", "A3", "A5", "A7", "A9",
    "B2", "B4", "B6", "B8",
    "C1", "C3", "C5", "C8",
    "D2", "D4", "D6",
    "E1", "E3", "E5",
    "F2", "F5", "F7",
    "G3", "G6", "G9",
]

# Status pool — weighted so most flights are On Time
STATUS_POOL = [
    "On Time",
    "On Time",
    "On Time",
    "On Time",
    "On Time",
    "Delayed",
    "Delayed",
    "Boarding",
    "Landed",
    "Cancelled",
]
