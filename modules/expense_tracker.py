"""
expense_tracker.py

Logs day to day spending and checks it against a monthly budget.
Categories are just plain text (Food, Travel, Books, etc.) so you can
type whatever fits - no fixed dropdown list to worry about.
"""

from modules import storage
from modules import utils

EXPENSE_FILE = "expenses_data.json"
BUDGET_FILE = "budget_data.json"


def load_expenses():
    return storage.read_json(EXPENSE_FILE, [])


def save_expenses(expenses):
    storage.write_json(EXPENSE_FILE, expenses)


def load_budget():
    data = storage.read_json(BUDGET_FILE, {"monthly_budget": 0})
    return data.get("monthly_budget", 0)


def save_budget(amount):
    storage.write_json(BUDGET_FILE, {"monthly_budget": amount})


def add_expense(expenses, amount, category, note="", date=None):
    if amount <= 0:
        print("Amount must be more than zero.")
        return False

    if date is None:
        date = utils.today_string()

    new_expense = {
        "amount": round(amount, 2),
        "category": category,
        "note": note,
        "date": date,
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    storage.write_log("Expense logged: " + str(amount) + " under " + category)
    return True


def _matches_month_year(expense, month, year):
    day, mon, yr = expense["date"].split("-")
    if month is not None and int(mon) != month:
        return False
    if year is not None and int(yr) != year:
        return False
    return True


def total_spent(expenses, month=None, year=None):
    matching = [e["amount"] for e in expenses if _matches_month_year(e, month, year)]
    return round(sum(matching), 2)


def category_totals(expenses, month=None, year=None):
    """Returns a dict like {'Food': 450, 'Travel': 120}."""
    totals = {}
    for expense in expenses:
        if not _matches_month_year(expense, month, year):
            continue
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]

    # round all the totals at the end
    for category in totals:
        totals[category] = round(totals[category], 2)

    return totals


def budget_status(expenses, budget, month, year):
    spent = total_spent(expenses, month, year)

    if budget <= 0:
        return {"spent": spent, "budget": 0, "status": "No budget set"}

    remaining = round(budget - spent, 2)

    if spent > budget:
        status = "OVER BUDGET"
    elif spent >= budget * 0.8:
        status = "APPROACHING LIMIT"
    else:
        status = "OK"

    return {
        "spent": spent,
        "budget": budget,
        "remaining": remaining,
        "status": status,
    }
