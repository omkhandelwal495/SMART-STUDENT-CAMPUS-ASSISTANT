"""
planner.py

Basic task/assignment planner - add a task with a deadline and
priority, view what's pending, see what's overdue, and mark things
done once they're finished.
"""

from modules import storage
from modules import utils

FILE_NAME = "planner_data.json"

VALID_PRIORITIES = ["High", "Medium", "Low"]
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def load_tasks():
    return storage.read_json(FILE_NAME, [])


def save_tasks(tasks):
    storage.write_json(FILE_NAME, tasks)


def _next_id(tasks):
    if len(tasks) == 0:
        return 1
    ids = [t["id"] for t in tasks]
    return max(ids) + 1


def add_task(tasks, title, deadline, priority="Medium", subject=""):
    priority = priority.strip().capitalize()
    if priority not in VALID_PRIORITIES:
        priority = "Medium"

    new_task = {
        "id": _next_id(tasks),
        "title": title,
        "subject": subject,
        "deadline": deadline,
        "priority": priority,
        "done": False,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    storage.write_log("Task added: " + title + " due " + deadline)
    return new_task


def mark_done(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            return True
    return False


def delete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return True
    return False


def pending_tasks(tasks):
    """Returns tasks that are not done yet, soonest deadline first."""
    pending = [t for t in tasks if not t["done"]]
    pending.sort(key=lambda t: (utils.parse_date(t["deadline"]), PRIORITY_ORDER[t["priority"]]))
    return pending


def overdue_tasks(tasks):
    return [t for t in pending_tasks(tasks) if utils.days_until(t["deadline"]) < 0]


def due_soon_tasks(tasks, within_days=3):
    return [t for t in pending_tasks(tasks) if 0 <= utils.days_until(t["deadline"]) <= within_days]


def completed_tasks(tasks):
    return [t for t in tasks if t["done"]]
