"""
academic.py

Keeps track of subject results and works out GPA / CGPA.
No classes here on purpose - just simple functions that take the
records list in and give it back out, which is easier to follow and
easier to test one piece at a time.
"""

from modules import storage

FILE_NAME = "academic_data.json"

# standard 10 point grading scale
GRADE_POINTS = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "F": 0,
}


def load_records():
    return storage.read_json(FILE_NAME, [])


def save_records(records):
    storage.write_json(FILE_NAME, records)


def add_subject(records, semester, subject_name, credits, grade):
    """
    Adds one subject result to the records list and saves it.
    Returns True if it worked, False if something was wrong with the
    input (bad grade or bad credits).
    """
    grade = grade.upper().strip()

    if grade not in GRADE_POINTS:
        print("That grade is not valid. Use one of:", list(GRADE_POINTS.keys()))
        return False

    if credits <= 0:
        print("Credits must be a positive number.")
        return False

    new_entry = {
        "semester": semester,
        "subject": subject_name,
        "credits": credits,
        "grade": grade,
    }
    records.append(new_entry)
    save_records(records)
    storage.write_log("Added subject " + subject_name + " for " + semester)
    return True


def calculate_gpa(records):
    """Works out GPA for whatever list of records is passed in."""
    if len(records) == 0:
        return 0.0

    total_points = 0
    total_credits = 0

    for record in records:
        points = GRADE_POINTS[record["grade"]]
        credits = record["credits"]
        total_points = total_points + (points * credits)
        total_credits = total_credits + credits

    if total_credits == 0:
        return 0.0

    return round(total_points / total_credits, 2)


def get_records_for_semester(records, semester):
    matching = []
    for record in records:
        if record["semester"] == semester:
            matching.append(record)
    return matching


def gpa_for_semester(records, semester):
    semester_records = get_records_for_semester(records, semester)
    return calculate_gpa(semester_records)


def cgpa_overall(records):
    return calculate_gpa(records)


def list_semesters(records):
    """Returns a list of unique semester names, in the order first seen."""
    semesters = []
    for record in records:
        if record["semester"] not in semesters:
            semesters.append(record["semester"])
    return semesters
