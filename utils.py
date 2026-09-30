"""
utils.py

Small helper functions used by more than one module, mostly for
getting valid input from the user in the console menu.
"""

import os
import datetime


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_header(title):
    print("")
    print("=" * 50)
    print(title.center(50))
    print("=" * 50)


def get_valid_number(prompt, minimum=0):
    """Keep asking until the user types a real number."""
    while True:
        text = input(prompt)
        try:
            number = float(text)
            if number < minimum:
                print("Value cannot be less than", minimum, "- try again.")
            else:
                return number
        except ValueError:
            print("That is not a valid number. Try again.")


def get_valid_date(prompt, allow_blank=False):
    """Expects date as DD-MM-YYYY, returns it as a string."""
    while True:
        text = input(prompt).strip()
        if allow_blank and text == "":
            return ""
        try:
            datetime.datetime.strptime(text, "%d-%m-%Y")
            return text
        except ValueError:
            print("Please enter the date as DD-MM-YYYY, for example 25-09-2026")


def today_string():
    return datetime.datetime.now().strftime("%d-%m-%Y")


def parse_date(date_text):
    return datetime.datetime.strptime(date_text, "%d-%m-%Y")


def days_until(date_text):
    """Returns how many days are left until date_text. Negative = overdue."""
    target_date = parse_date(date_text)
    today = datetime.datetime.now()
    difference = target_date - today
    return difference.days
