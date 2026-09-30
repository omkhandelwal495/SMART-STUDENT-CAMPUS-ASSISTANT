"""
Tests for the academic module. Uses a separate test data file so it
never touches the real academic_data.json.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import academic


class TestAcademic(unittest.TestCase):

    def setUp(self):
        academic.FILE_NAME = "test_academic_data.json"
        self.records = []

    def tearDown(self):
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "test_academic_data.json",
        )
        if os.path.exists(path):
            os.remove(path)

    def test_add_subject_and_gpa(self):
        academic.add_subject(self.records, "Sem1", "Maths", 4, "A")
        academic.add_subject(self.records, "Sem1", "Physics", 3, "O")
        gpa = academic.gpa_for_semester(self.records, "Sem1")
        # (4*8 + 3*10) / 7 = 8.857...
        self.assertAlmostEqual(gpa, 8.86, places=1)

    def test_invalid_grade_returns_false(self):
        result = academic.add_subject(self.records, "Sem1", "Chemistry", 3, "Z")
        self.assertFalse(result)
        self.assertEqual(len(self.records), 0)

    def test_zero_credits_returns_false(self):
        result = academic.add_subject(self.records, "Sem1", "Chemistry", 0, "A")
        self.assertFalse(result)

    def test_gpa_with_no_records_is_zero(self):
        self.assertEqual(academic.gpa_for_semester(self.records, "SemX"), 0.0)

    def test_list_semesters(self):
        academic.add_subject(self.records, "Sem1", "Maths", 4, "A")
        academic.add_subject(self.records, "Sem2", "Physics", 3, "O")
        semesters = academic.list_semesters(self.records)
        self.assertEqual(semesters, ["Sem1", "Sem2"])


if __name__ == "__main__":
    unittest.main()
