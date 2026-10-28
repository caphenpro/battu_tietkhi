"""Regression tests for the precise lunar-month calculation."""
import unittest

from amlich.precise import leap_month_precise, lunar_months_precise, solar_terms


class PreciseLunarCalendarTests(unittest.TestCase):
    def test_known_leap_months(self):
        self.assertEqual(leap_month_precise(2025, tz=7), 6)
        self.assertIsNone(leap_month_precise(2024, tz=7))

    def test_special_2033_calendar(self):
        # 2033 is a known edge case in which a lunar month can contain
        # two major solar terms; month numbering must not rely on term names.
        self.assertEqual(leap_month_precise(2033, tz=7), 11)

    def test_precise_month_lengths_and_count(self):
        for year in (2023, 2024, 2025, 2033):
            months = lunar_months_precise(year, tz=7)
            self.assertIn(len(months), (12, 13), msg=f"year={year}")
            for month in months:
                self.assertIn(month.length, (29, 30), msg=f"year={year}, month={month}")

    def test_solar_terms_cover_requested_local_year(self):
        for year in (2023, 2024, 2025, 2033):
            terms = solar_terms(year, tz=7)
            self.assertEqual(len(terms), 24, msg=f"year={year}")
            times = [dt for _, dt in terms]
            self.assertEqual(times, sorted(times), msg=f"year={year}")
            self.assertTrue(all(dt.year == year for dt in times), msg=f"year={year}")


if __name__ == "__main__":
    unittest.main()
