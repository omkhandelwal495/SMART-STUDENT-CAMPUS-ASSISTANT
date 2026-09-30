import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import expense_tracker


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        expense_tracker.EXPENSE_FILE = "test_expenses_data.json"
        self.expenses = []

    def tearDown(self):
        data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
        )
        path = os.path.join(data_dir, "test_expenses_data.json")
        if os.path.exists(path):
            os.remove(path)

    def test_negative_amount_returns_false(self):
        result = expense_tracker.add_expense(self.expenses, -50, "Food")
        self.assertFalse(result)
        self.assertEqual(len(self.expenses), 0)

    def test_total_spent(self):
        expense_tracker.add_expense(self.expenses, 100, "Food", date="01-09-2026")
        expense_tracker.add_expense(self.expenses, 50, "Travel", date="15-09-2026")
        total = expense_tracker.total_spent(self.expenses, month=9, year=2026)
        self.assertEqual(total, 150)

    def test_budget_status_over_budget(self):
        expense_tracker.add_expense(self.expenses, 150, "Food", date="05-09-2026")
        status = expense_tracker.budget_status(self.expenses, 100, 9, 2026)
        self.assertEqual(status["status"], "OVER BUDGET")

    def test_category_totals(self):
        expense_tracker.add_expense(self.expenses, 100, "Food", date="01-09-2026")
        expense_tracker.add_expense(self.expenses, 40, "Food", date="02-09-2026")
        totals = expense_tracker.category_totals(self.expenses, month=9, year=2026)
        self.assertEqual(totals["Food"], 140)


if __name__ == "__main__":
    unittest.main()
