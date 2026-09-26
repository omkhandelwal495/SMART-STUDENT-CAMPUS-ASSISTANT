# Smart Student Campus Assistant

A console-based Python application that brings together four things a
college student normally tracks separately: academic performance,
campus information, personal expenses, and a day-to-day task planner.

Built as a course project (VITyarthi - Build Your Own Project) to
apply core programming concepts - functions, file handling, JSON data
storage, input validation and basic testing - to a genuinely useful,
everyday problem.

## Why this project

Most students end up using 3-4 different apps just to keep track of
their semester: a spreadsheet for expenses, sticky notes for
deadlines, WhatsApp groups for campus announcements, and nothing at
all for tracking GPA. This project puts all four into one simple tool
that runs from the terminal and doesn't need internet access or an
account of any kind.

## Features

### 1. Academic Summary
- Add subject-wise results (credits + grade) per semester
- Automatic GPA calculation per semester
- Overall CGPA across all semesters recorded so far

### 2. Campus Info
- Searchable directory of departments, faculty and their subjects
- List of campus facilities (library hours, canteen timings, etc.)
- Upcoming events board - anyone can add a new event/announcement

### 3. Expense Tracker
- Log expenses with category, amount, date and an optional note
- Set a monthly budget and get a status check (OK / Approaching limit / Over budget)
- Category-wise spending breakdown for the current month

### 4. Planner
- Add tasks/assignments with a deadline, priority and related subject
- View pending tasks, sorted by nearest deadline first
- Separate view for overdue tasks so nothing slips through
- Mark tasks as done

## Technologies / Tools Used

- **Python 3.9+** (standard library only)
- Only the built-in modules `json`, `os`, and `datetime` are used
  for data storage, file handling and dates
- **unittest** (also built into Python) for the automated tests
- **Git** for version control

The code is written in a simple, functional style - plain functions
that take data in and return it out, ordinary `for` loops, and basic
`if/else` checks - rather than classes, so it's easy to read top to
bottom and easy to explain during evaluation.

## Project Structure

```
SmartCampusAssistant/
├── main.py                     # CLI entry point / menu system
├── modules/
│   ├── academic.py             # GPA/CGPA functions
│   ├── campus_info.py          # directory + search functions
│   ├── expense_tracker.py      # expense + budget functions
│   ├── planner.py              # task/deadline functions
│   ├── storage.py              # read/write json + simple log file
│   └── utils.py                # shared input validation helpers
├── data/                       # json data files
├── tests/                      # unittest test cases per module
├── README.md
├── statement.md
└── requirements.txt
```

## Steps to Install & Run

1. Make sure Python 3.9 or newer is installed:
   ```
   python --version
   ```
2. Clone this repository:
   ```
   git clone <your-repo-url>
   cd SmartCampusAssistant
   ```
3. No external packages are needed (standard library only), so there's
   nothing to `pip install`. If you'd still like a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate        # on Windows: venv\Scripts\activate
   ```
4. Run the app:
   ```
   python main.py
   ```
5. Follow the on-screen menu - type a number and press Enter.

## Instructions for Testing

Run all tests from the project root:
```
python -m unittest discover tests
```
Or run a single module's tests, e.g.:
```
python -m unittest tests.test_planner
```
Tests use temporary data files (prefixed `test_`) so they never touch
your real academic/expense/planner data.

## Sample Data

`data/campus_data.json` comes with a few sample departments, faculty
members, facilities and events so the Campus Info section isn't empty
on first run. Academic, expense and planner data start empty and fill
up as you use the app.

## Non-Functional Notes

- **Performance:** data is loaded once when the app starts and kept in
  a normal Python list/dict in memory, only writing back to disk when
  something actually changes.
- **Security:** every number/date typed in by the user is checked
  before it's used; there's no `eval`, `exec`, or shell command
  anywhere in the code.
- **Reliability:** file reading is wrapped in try/except so a missing
  or damaged json file doesn't crash the app on startup - it just
  falls back to an empty list.
- **Usability:** menu-driven CLI with clear prompts, and it asks again
  instead of crashing if you type something invalid.
- **Maintainability:** each feature lives in its own file with plain
  functions, so adding a fifth feature later would mean adding one new
  file rather than changing the existing ones.
- **Logging:** key actions (adding a subject, an expense, a task) are
  written with a timestamp to `campus_assistant.log` for a basic
  activity record.

## Future Enhancements

- Export academic/expense summaries to PDF or Excel
- A simple Tkinter or web front-end instead of the command line
- Reminders/notifications for deadlines due today
- Multi-user support (currently single-user, local data only)

## Author

Built as an individual submission for the flipped-classroom project
evaluation.
