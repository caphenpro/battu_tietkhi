"""Kiểm thử bộ lịch âm nhanh (không cần astronomy-engine)."""
import unittest

from amlich import leap_month, lunar_months


class LunarCalendarTests(unittest.TestCase):
    def test_known_leap_months(self):
        self.assertEqual(leap_month(2025), 6)
        self.assertIsNone(leap_month(2024))

    def test_lunar_month_lengths_are_29_or_30_days(self):
        for year in (2023, 2024, 2025, 2033):
            for month in lunar_months(year):
                self.assertIn(month.length, (29, 30))

    def test_cycle_has_12_or_13_months(self):
        for year in (2023, 2024, 2025, 2033):
            self.assertIn(len(lunar_months(year)), (12, 13))


if __name__ == "__main__":
    unittest.main()
