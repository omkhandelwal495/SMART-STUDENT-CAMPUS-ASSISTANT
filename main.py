"""
main.py

This is the file you actually run - python main.py - and it just
shows a text menu in the terminal. Type a number, hit enter, it takes
you to that part of the app (academics / campus info / expenses /
planner). All the real logic lives in the modules/ folder, this file
mostly just asks questions and prints answers.

Wrote this bit by bit while testing each module separately, so the
four menu functions below aren't 100% identical in style - some ask
for input first then validate, others do it the other way round.
Works fine either way, just didn't bother going back to make them
match exactly.
"""

from modules import academic
from modules import campus_info
from modules import expense_tracker
from modules import planner
from modules import utils
import datetime


def academic_menu(records):
    while True:
        utils.print_header("Academic Summary")
        print("1. Add subject result")
        print("2. View GPA for a semester")
        print("3. View overall CGPA")
        print("4. Back to main menu")
        choice = input("> ").strip()

        if choice == "1":
            sem = input("Semester (example: Sem3): ").strip()
            subj = input("Subject name: ").strip()
            credits = utils.get_valid_number("Credits: ", minimum=1)
            grade = input("Grade (O / A+ / A / B+ / B / C / F): ").strip()

            # add_subject already prints its own error if grade/credits
            # are wrong, so we only need to react when it actually worked
            added_ok = academic.add_subject(records, sem, subj, credits, grade)
            if added_ok:
                print("Saved.")

        elif choice == "2":
            sem = input("Which semester? ").strip()
            gpa = academic.gpa_for_semester(records, sem)
            print("GPA for", sem, "is", gpa)

        elif choice == "3":
            print("Overall CGPA:", academic.cgpa_overall(records))

        elif choice == "4":
            return

        else:
            print("Not a valid option, pick a number from the menu above.")


def campus_menu(data):
    while True:
        utils.print_header("Campus Info")
        print("1. Search campus info")
        print("2. List upcoming events")
        print("3. List facilities")
        print("4. Add an event")
        print("5. Back to main menu")
        choice = input("> ").strip()

        if choice == "1":
            keyword = input("Search for: ").strip()
            results = campus_info.search_info(data, keyword)

            found_anything = False
            for category, items in results.items():
                if not items:
                    continue
                found_anything = True
                print("\n" + category.title() + ":")
                for item in items:
                    print("  -", item)

            if not found_anything:
                print("Nothing matched that search, try a different keyword.")

        elif choice == "2":
            events = campus_info.list_events(data)
            if not events:
                print("No events listed yet.")
            for ev in events:
                print("  -", ev["title"], "(" + ev["date"] + ")")

        elif choice == "3":
            for fac in campus_info.list_facilities(data):
                info = fac.get("info", "")
                print("  -", fac["name"] + ":", info)

        elif choice == "4":
            title = input("Event title: ").strip()
            date = input("Date (example: 15-10-2026): ").strip()
            desc = input("Short description: ").strip()
            campus_info.add_event(data, title, date, desc)
            print("Event added.")

        elif choice == "5":
            return

        else:
            print("Not a valid option, pick a number from the menu above.")


def expense_menu(expenses, budget):
    while True:
        utils.print_header("Expense Tracker")
        print("1. Add expense")
        print("2. Set monthly budget")
        print("3. View this month's status")
        print("4. Category breakdown (this month)")
        print("5. Back to main menu")
        choice = input("> ").strip()

        if choice == "1":
            amt = utils.get_valid_number("Amount spent: Rs. ", minimum=0.01)
            cat = input("Category (Food / Travel / Books / Hostel / Other): ").strip()
            note = input("Note (optional, press enter to skip): ").strip()
            if expense_tracker.add_expense(expenses, amt, cat, note):
                print("Logged.")

        elif choice == "2":
            amt = utils.get_valid_number("Set monthly budget: Rs. ")
            expense_tracker.save_budget(amt)
            budget = amt  # keep the local copy in sync too
            print("Budget updated.")

        elif choice == "3":
            now = datetime.datetime.now()
            status = expense_tracker.budget_status(expenses, budget, now.month, now.year)
            print("Spent so far this month: Rs.", status["spent"])
            if status["budget"] > 0:
                print("Budget: Rs.", status["budget"], " | Status:", status["status"])
            else:
                print("(no budget set yet - option 2 lets you set one)")

        elif choice == "4":
            now = datetime.datetime.now()
            totals = expense_tracker.category_totals(expenses, now.month, now.year)
            if not totals:
                print("Nothing logged this month so far.")
            else:
                for cat in totals:
                    print("  " + cat + ":", "Rs.", totals[cat])

        elif choice == "5":
            return budget

        else:
            print("Not a valid option, pick a number from the menu above.")


def planner_menu(tasks):
    while True:
        utils.print_header("Planner")
        print("1. Add task")
        print("2. View pending tasks")
        print("3. View overdue tasks")
        print("4. Mark task as done")
        print("5. Back to main menu")
        choice = input("> ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            subject = input("Related subject (optional): ").strip()
            deadline = utils.get_valid_date("Deadline (DD-MM-YYYY): ")
            priority = input("Priority (High / Medium / Low) [Medium]: ").strip()
            if priority == "":
                priority = "Medium"
            planner.add_task(tasks, title, deadline, priority, subject)
            print("Task added.")

        elif choice == "2":
            pending = planner.pending_tasks(tasks)
            if not pending:
                print("Nothing pending right now.")
            for t in pending:
                line = "  [" + str(t["id"]) + "] " + t["title"]
                line += " - due " + t["deadline"] + " (" + t["priority"] + ")"
                print(line)

        elif choice == "3":
            overdue = planner.overdue_tasks(tasks)
            if not overdue:
                print("Nothing overdue - good job staying on top of it.")
            for t in overdue:
                print("  [" + str(t["id"]) + "]", t["title"], "- was due", t["deadline"])

        elif choice == "4":
            raw = input("Task id to mark done: ").strip()
            if not raw.isdigit():
                print("That's not a task id, needs to be a number.")
                continue
            if planner.mark_done(tasks, int(raw)):
                print("Marked as done.")
            else:
                print("Couldn't find a task with that id.")

        elif choice == "5":
            return

        else:
            print("Not a valid option, pick a number from the menu above.")


def run_app():
    utils.print_header("SMART STUDENT CAMPUS ASSISTANT")
    print("Type the number of what you want and hit enter. Ctrl+C quits anytime.")

    # pull everything in once at startup - each menu just works off
    # these lists/dicts in memory and the modules handle saving
    academic_records = academic.load_records()
    campus_data = campus_info.load_data()
    expenses = expense_tracker.load_expenses()
    budget = expense_tracker.load_budget()
    tasks = planner.load_tasks()

    while True:
        print()
        print("Main Menu")
        print("1. Academic Summary")
        print("2. Campus Info")
        print("3. Expense Tracker")
        print("4. Planner")
        print("5. Exit")
        choice = input("> ").strip()

        if choice == "1":
            academic_menu(academic_records)
        elif choice == "2":
            campus_menu(campus_data)
        elif choice == "3":
            budget = expense_menu(expenses, budget)  # returns updated budget
        elif choice == "4":
            planner_menu(tasks)
        elif choice == "5":
            print("Bye, good luck with the semester.")
            break
        else:
            print("Didn't get that - type a number between 1 and 5.")


if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        print()
        print("Closed. See you next time.")
