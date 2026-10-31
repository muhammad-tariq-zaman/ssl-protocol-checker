import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import grade, probe


class TestProtocolChecker(unittest.TestCase):
    def test_grade_a(self):
        self.assertEqual(grade({"TLSv1.3": "supported", "TLSv1.2": "supported",
                                "TLSv1.1": "rejected", "TLSv1": "rejected"}), "A")

    def test_grade_b(self):
        self.assertEqual(grade({"TLSv1.3": "rejected", "TLSv1.2": "supported",
                                "TLSv1.1": "rejected", "TLSv1": "rejected"}), "B")

    def test_grade_c_for_old_only(self):
        self.assertEqual(grade({"TLSv1.3": "rejected", "TLSv1.2": "rejected",
                                "TLSv1.1": "supported", "TLSv1": "rejected"}), "C")

    def test_closed_port_all_error(self):
        results = probe("127.0.0.1", 9, timeout=2.0)
        self.assertTrue(all(state == "error" for state in results.values()))
        self.assertEqual(grade(results), "F")
