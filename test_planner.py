import os
import sys
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import planner


class TestPlanner(unittest.TestCase):

    def setUp(self):
        planner.FILE_NAME = "test_planner_data.json"
        self.tasks = []

    def tearDown(self):
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "test_planner_data.json",
        )
        if os.path.exists(path):
            os.remove(path)

    def future_date(self, days):
        return (datetime.now() + timedelta(days=days)).strftime("%d-%m-%Y")

    def test_add_and_mark_done(self):
        task = planner.add_task(self.tasks, "Submit assignment", self.future_date(2), "High", "DBMS")
        self.assertFalse(task["done"])
        worked = planner.mark_done(self.tasks, task["id"])
        self.assertTrue(worked)
        self.assertTrue(self.tasks[0]["done"])

    def test_pending_excludes_done(self):
        task_a = planner.add_task(self.tasks, "Task A", self.future_date(1))
        planner.add_task(self.tasks, "Task B", self.future_date(2))
        planner.mark_done(self.tasks, task_a["id"])
        pending = planner.pending_tasks(self.tasks)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["title"], "Task B")

    def test_overdue_detection(self):
        planner.add_task(self.tasks, "Late task", self.future_date(-3))
        overdue = planner.overdue_tasks(self.tasks)
        self.assertEqual(len(overdue), 1)

    def test_mark_done_invalid_id_returns_false(self):
        worked = planner.mark_done(self.tasks, 999)
        self.assertFalse(worked)


if __name__ == "__main__":
    unittest.main()
