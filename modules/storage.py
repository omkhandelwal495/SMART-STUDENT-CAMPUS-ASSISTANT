"""
storage.py

Just two functions: one to read a JSON file, one to write a JSON file.
Everything else in this project uses these two so we don't repeat the
same open()/json.load() code again and again.
"""

import json
import os

# folder where this file lives -> go up one level -> data folder
THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(THIS_FOLDER, "data")


def read_json(filename, default_value):
    """
    Reads a json file from the data folder.
    If the file doesn't exist yet, or has bad data in it, we just
    return default_value instead of crashing the program.
    """
    file_path = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(file_path):
        return default_value

    try:
        file = open(file_path, "r")
        text = file.read()
        file.close()

        if text.strip() == "":
            return default_value

        return json.loads(text)
    except Exception:
        print("Warning: could not read", filename, "- using default data.")
        return default_value


def write_json(filename, data):
    """Saves data as json inside the data folder."""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    file_path = os.path.join(DATA_FOLDER, filename)

    try:
        file = open(file_path, "w")
        json.dump(data, file, indent=2)
        file.close()
        return True
    except Exception:
        print("Warning: could not save", filename)
        return False


def write_log(message):
    """
    Very simple activity log. Just appends one line with a timestamp
    to campus_assistant.log in the project folder. Not fancy, but it
    does the job of keeping a record of what happened.
    """
    import datetime
    log_path = os.path.join(THIS_FOLDER, "campus_assistant.log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        file = open(log_path, "a")
        file.write("[" + timestamp + "] " + message + "\n")
        file.close()
    except Exception:
        pass
