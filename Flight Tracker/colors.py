# colors.py
# Sample Terminal color codes used across the app.

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# Maps each flight status to its display color
STATUS_COLORS = {
    "On Time":   GREEN,
    "Boarding":  BLUE,
    "Delayed":   RED,
    "Landed":    GREY,
    "Departed":  GREY,
    "Cancelled": YELLOW,
}
