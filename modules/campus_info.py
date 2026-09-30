"""
campus_info.py

A searchable mini directory for the campus - departments, faculty,
facilities and events. The actual data sits in data/campus_data.json
so it can be edited by hand too, this file just knows how to read it,
search it, and add new entries.
"""

from modules import storage

FILE_NAME = "campus_data.json"

EMPTY_DATA = {
    "departments": [],
    "faculty": [],
    "facilities": [],
    "events": [],
}


def load_data():
    data = storage.read_json(FILE_NAME, EMPTY_DATA)
    # make sure every key exists, in case an older file is missing one
    for key in EMPTY_DATA:
        if key not in data:
            data[key] = []
    return data


def save_data(data):
    storage.write_json(FILE_NAME, data)


def list_departments(data):
    return data["departments"]


def list_faculty(data):
    return data["faculty"]


def list_facilities(data):
    return data["facilities"]


def list_events(data):
    return data["events"]


def search_info(data, keyword):
    """
    Looks for keyword inside department names, faculty names/subjects,
    facility names, and event titles. Simple 'is this text inside
    that text' search, nothing fancy.
    """
    keyword = keyword.lower().strip()

    results = {
        "departments": [],
        "faculty": [],
        "facilities": [],
        "events": [],
    }

    for dept in data["departments"]:
        if keyword in dept["name"].lower():
            results["departments"].append(dept)

    for person in data["faculty"]:
        text = person["name"] + " " + person["department"] + " " + person.get("subject", "")
        if keyword in text.lower():
            results["faculty"].append(person)

    for facility in data["facilities"]:
        text = facility["name"] + " " + facility.get("info", "")
        if keyword in text.lower():
            results["facilities"].append(facility)

    for event in data["events"]:
        text = event["title"] + " " + event.get("description", "")
        if keyword in text.lower():
            results["events"].append(event)

    return results


def add_event(data, title, date, description):
    new_event = {"title": title, "date": date, "description": description}
    data["events"].append(new_event)
    save_data(data)
    storage.write_log("Added event: " + title)
    return data
